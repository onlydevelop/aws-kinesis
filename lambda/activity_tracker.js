var AWS = require('aws-sdk');
AWS.config.update({region: 'ap-south-1'});
const docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10', region: 'ap-south-1'});

exports.handler = (event, context, callback) => {
    event.Records.forEach(function(record) {
        var payload = new Buffer(record.kinesis.data, 'base64').toString('ascii');
        console.log('Decoded payload:', payload);
        var params = {
          TableName: 'activity',
          Item: JSON.parse(payload)
        };

        docClient.put(params, function(err, data) {
          if (err) {
            console.log(err);
            return callback(null, 'Error');
          } else {
            console.log(data);
            return callback(null, 'Success');
          }
        });
    });
};


