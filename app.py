import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    print(f"Chave da OpenAI: {openai.api_key}") # Esta é a linha que você deve adicionar


    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": incoming_msg}
            ]
        )
        bot_response = completion.choices[0].message.content
        msg.body(bot_response)
    except Exception as e:
        print(f"Erro ao chamar a OpenAI: {e}")
        msg.body("Desculpe, houve um erro ao processar sua mensagem.")

    return Response(str(resp), mimetype="application/xml")

if __name__ == '__main__':
    app.run(debug=False)
