import nexmo



client = nexmo.Client(key='a59d3fa4', secret='PsNbJalLH1B5ka5V')

number = input("Enter the phone number")
message = input("Enter the message ")

response = client.send_message({'from':'9424113570','to':number,'text':message})
response = response['messages'][0]

if response['status']=='0':
        print('send message ',response['message-id'])

else:
        print('Error:', response['error-text'])
