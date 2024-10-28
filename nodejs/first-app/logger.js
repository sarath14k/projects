var url = 'http://mylogger.io/log'

function log(message){
    // Send HTTP req
    console.log(message + ' KINDI');
}

module.exports.log = log;
module.exports.endPoint = url;