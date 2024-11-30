from django.shortcuts import render, get_object_or_404
from .models import Message
from staff_app.models import CoustomUser,Student
from django.db.models import Max,Q
from django.http import JsonResponse

def chat_view(request, conversation_id):
    receiver= get_object_or_404(CoustomUser, roll_number=conversation_id)
    sender_id= get_object_or_404(CoustomUser, id=request.user.id )
    sender_roll=sender_id.roll_number
    print(receiver,sender_id)
    
    # Load all messages between the logged-in user and the receiver
    chats = Message.objects.filter(
       Q(sender=sender_id,receiver=receiver) | Q(sender=receiver, receiver=sender_id)
    ).order_by('timestamp')
    print("************************************************************")
    print("ALL chats")
    print(chats)
    print("**********************************************************")
    print()
    print("************************************************************")
    print("Unique users")
    unique_receivers = CoustomUser.objects.filter(Q(received_messages__sender__roll_number=sender_roll)| Q(sent_messages__receiver__roll_number=sender_roll)).distinct()
    for i in unique_receivers:
        print(i.id)
    print("**********************************************************")
    
    print("************************************************************")
    print("last_messages")
    last_messages = Message.objects.filter(Q(sender__roll_number=sender_roll)|Q(receiver__roll_number=sender_roll)).values('sender','receiver').annotate(last_chat=Max('timestamp')).distinct()
    print("last messges are:",last_messages)
    for i in last_messages:
        print(i)
    print("************************************************************")
    last_chats = []
    processed_pairs = set() 
    for msg in last_messages:
        
        actual_sender=msg['sender']
        actual_receiver=msg['receiver']
        chat_pair=tuple(sorted([actual_sender,actual_receiver]))
        if chat_pair not in processed_pairs:
            
            last_message = Message.objects.filter(
                Q(sender=actual_sender,receiver=actual_receiver,timestamp=msg['last_chat'])|
                Q(sender=actual_receiver,receiver=actual_sender,timestamp=msg['last_chat'])
                ).select_related('receiver__student','sender__student').distinct().first()
            
            
            print("______________________________________________________________")
        
            print(last_message)
            print("______________________________________________________________")
            if last_message:
                # Normalize sender and receiver: make the logged-in user always the sender
                if last_message.sender != sender_id:
                    last_message.sender, last_message.receiver = last_message.receiver, last_message.sender
                # last_message.= Student.objects.get(roll_number =receiver )
                last_chats.append( {'message': last_message,
                        'receiver_profile': last_message.receiver if last_message.receiver != sender_id else last_message.sender,
                        'user': last_message.receiver if last_message.receiver != sender_id else last_message.sender,})
            processed_pairs.add(chat_pair)
    if request.user.is_student==True:
                return render(request, 'user_pages/user_chat.html', {
                    'receiver': receiver,
                    'chats': chats,
                    'unique_receivers':unique_receivers,
                    'last_chats': last_chats
                    
                        })
    else:
                return render(request, 'staff_pages/staff_chat.html', {
                        'receiver': receiver,
                        'chats': chats,
                        'unique_receivers':unique_receivers,
                        'last_chats': last_chats
                    })
    



def loadchat(request):
    current_user = request.user
    
    # Get unique receivers with the last message exchanged
    last_messages = (Message.objects.filter(sender=current_user).values('receiver').annotate(last_chat=Max('timestamp')))
    print(last_messages)
    # Retrieve the last message content and receiver details
    last_chats = []
    for msg in last_messages:
        last_message = Message.objects.filter(
            sender=current_user, receiver=msg['receiver'], timestamp=msg['last_chat']
        ).first()
        # user_id=CoustomUser.objects.get(msg['receiver'])
        if last_message:
            last_chats.append({'message':last_message})
    unique_receivers = CoustomUser.objects.filter(received_messages__sender=current_user).distinct()
    context = {'last_chats': last_chats,'unique_receivers':unique_receivers  }
    if request.user.is_student==True:
        return render(request, 'user_pages/user_chat.html',context)
    else:
         return render(request, 'staff_pages/staff_chat.html',context)



# def loadchat(request):
#     sender_id=request.user.id
#     sender = CoustomUser.objects.get(id=sender_id)
#     unique_receivers = CoustomUser.objects.filter(received_messages__sender=sender).distinct()
    
#     return render(request,'chat2.html',{'unique_receivers':unique_receivers})