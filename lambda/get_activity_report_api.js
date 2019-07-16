var AWS = require('aws-sdk');
AWS.config.update({region: 'ap-south-1'});
const docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10', region: 'ap-south-1'});

exports.handler = (event, context, callback) => {

    if (event.queryStringParameters != undefined) {
        var subject = event.queryStringParameters.subject;
        var topic = event.queryStringParameters.topic;
    }

    let queryParameters = {
        TableName: 'activity',
        KeyConditionExpression: "#SubTopicKey = :sub and #Timestamp > :Timestamp",
        FilterExpression: '#Correct = :Correct',
        ExpressionAttributeNames:{
            "#SubTopicKey": "sub_topic",
            "#Timestamp": "start_time",
            "#Correct": "correct"
        },
        ExpressionAttributeValues: {
            ":sub": subject + '-' + topic,
            ":Timestamp": Math.floor((new Date().getTime() - (7*24*60*60*1000))/1000),
            ":Correct": "yes"
        }
    };

    docClient.query(queryParameters, function(err,data){
        if(err){
            var error = {
                'statusCode': 500,
                'body': err
            }
            callback(err, null);
        }else{
            var correct = data.Count;
            var incorrect = data.ScannedCount - data.Count;

            var response = {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': JSON.stringify([correct, incorrect])
            }
            callback(null,response);
        }
    });
};
