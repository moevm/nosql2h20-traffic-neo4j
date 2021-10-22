var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/* GET statistics page. */
router.get('/statistics', function(req, res, next) {
  res.render('statistics', { title: 'Express' });
});

module.exports = router;
