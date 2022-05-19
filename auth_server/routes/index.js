var express = require('express');
var router = express.Router();
const Query = require('../db').queryModel
const { endpoints,errorMessages } = require('../utils');
const verifyToken = require('./users').verifyToken

/* GET home page. */
router.get(
  '/', 
  function(req, res, next) {
    res.render('index', { title: 'Auth Server' });
  }
);

router.route('/query/:userId').get(
  verifyToken,
  function(req, res, next) {
    Query.find({user:req.params.userId}).then(
      response=>{
        return res.status(200).json(response)
      }
    ).catch(
      error=>{
        console.log(error)
        return res.status(500).send(errorMessages.FAILED_FETCH_QUERY)
      }
    )
  }
).put(
  verifyToken,
  function(req, res, next) {
    Query.findByIdAndUpdate(req.params.userId,req.body).then(
      response=>{
        return res.status(200).json(response)
      }
    ).catch(
      error=>{
        console.log(error)
        return res.status(500).send(errorMessages.FAILED_PUT_QUERY)
      }
    )
  }
).delete(
  verifyToken,
  function(req, res, next) {
    Query.findByIdAndDelete(req.params.userId).then(
      response=>{
        return res.status(200).json(response)
      }
    ).catch(
      error=>{
        console.log(error)
        return res.status(500).send(errorMessages.FAILED_DELETE_QUERY)
      }
    )
  }
)

router.route('/query').post(
  verifyToken,
  function(req, res, next) {
   Query.create(req.body).then(
      response=>{
        return res.status(200).json(response)
      }
    ).catch(
      error=>{
        console.log(error)
        return res.status(500).send(errorMessages.FAILED_POST_QUERY)
      }
    )
  }
)


module.exports = router;
