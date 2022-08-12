import json
from logging import exception
import logging
from flask import Flask, render_template
from flask import request
import pika

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        try:
            connection = pika.BlockingConnection(pika.URLParameters(
                'amqps://ksljhpzg:b-GA2Sl_VIivj8zYUR0h9oFopdQRwR8Q@rattlesnake.rmq.cloudamqp.com/ksljhpzg'))
            channel = connection.channel()
            channel.queue_declare(queue='wc_orders-in')
            channel.basic_publish(exchange='router',
                                  routing_key='orders',
                                  body=json.dumps(data))
            connection.close()
        except Exception as Argument:
            logging.exception('Error!')

        return 'OK', 200
    else:
        return 'Waiting for order'

if __name__ == '__main__':
    app.run()
