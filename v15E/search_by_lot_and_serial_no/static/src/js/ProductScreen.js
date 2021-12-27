odoo.define('search_by_lot_and_serial_no.ProductScreen', function(require) {
    'use strict';
    var core = require('web.core');
    var utils = require('web.utils');
    var PosDB = require('web.utils');
    var models = require('point_of_sale.models');
    var DB = require('point_of_sale.DB');
    var lot_ids;
    var prod_id;
    models.load_models([{
        model: 'stock.production.lot',
        fields: ['id', 'name', 'product_id'],
      loaded: function(self, lots) {
          self.lot_ids = lots;
//          prod_id = product_id;
      },
    }]);
    models.load_fields("product.product", "lot_ids");


    DB.include({
    init: function( options ){
        this._super(options);
        var self = this
        this.product_lot = {}
    },
//    add_products: function(products){
//        this._super(products);
//        if(!products instanceof Array){
//            products = [products]
//        }
//    },


    _product_search_string: function(product){
        var str = product.display_name;
        if (product.lot_ids) {
            str += '|' + product.lot_ids;
        }
        str  = product.id + ':' + str.replace(/:/g,'') + '\n';
        return str;
    },
    });
});