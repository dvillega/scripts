/**
 * Script to clear out data from S3
 * Devin Villegas
 */

"use strict";

var AWS   = require("aws-sdk"),
  config  = require('../config'),
  Q       = require('q'),
  _       = require('lodash-node');


var env_prefix = process.env.NODE_ENV ? 'production' : 'qa';

AWS.config.update({accessKeyId: config.get('aws_access_key_id'),
               secretAccessKey: config.get('aws_secret_access_key')});

var s3 = new AWS.S3({params: {Bucket: 'application_uploads'},
                     region: 'us-east-1'});

function getGaugeKeys() {
  var deferred  = Q.defer(),
    deleteKeys  = [];
  s3.listObjects({ Prefix: env_prefix + '/Gauge/'},
    function (err, data) {
      if (err) {
        console.log(err, err.stack);
      } else {
        data.Contents.forEach(function (elem) {
          if (elem.Key !== env_prefix + '/Gauge/') {
            var foo = {'Key': elem.Key};
            deleteKeys.push(foo);
          }
        });
        deferred.resolve(deleteKeys);
      }
    });
  return deferred.promise;
}

function deleteGaugeKeys(keys) {
  s3.deleteObjects({Delete: { Objects: keys} }, function (err, data) {
    if (err) {
      console.log(err, err.stack);
    } else {
      console.log(data);
    }
  });
}

getGaugeKeys().then(deleteGaugeKeys);

