var AWS = require('aws-sdk');
AWS.config.update({region: 'ap-south-1'});
const docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10', region: 'ap-south-1'});

exports.handler = (event, context, callback) => {

  var params = {
    TableName: 'activity',
    Item: JSON.parse(event.body)
  };


  var status = "";
  docClient.put(params, function(err, data) {
    if (err) {
      console.log(err);
      status = "Error";
    } else {

      status = "Success";
    }
  });

  var response = {
        "statusCode": 200,
        "body": status
    };
  callback(null, response);

};
