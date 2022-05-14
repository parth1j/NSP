var express = require('express');
var router = express.Router();
const Query = require('../db').queryModel
const { endpoints,errorMessages } = require('../utils');
/* GET home page. */
router.get(
  '/', 
  function(req, res, next) {
    res.render('index', { title: 'Auth Server' });
  }
);

router.get(
  '/query/:userId',
  function(req, res, next) {
    Query.find({user:req.params.userId}).then(
      response=>{

      }
    ).catch(
      error=>{
        
      }
    )
  }
)

router.post(
  '/query',
  function(req, res, next) {
   
  }
)

router.put(
  '/query',
  function(req, res, next) {
    
  }
)

router.delete(
  '/query',
  function(req, res, next) {
    
  }
)

module.exports = router;
