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
      loaded: function(self, lots, product_id) {
          lot_ids = lots;
//          prod_id = product_id;
        console.log("lot_ids-------->>>>>>...",lot_ids)
      },
    }]);

    DB.include({
    init: function( options ){
        this._super(options);
        var self = this
        console.log("lot_ids--------###########->>>",lot_ids)

//        this.product_by_old_barcode = {}
    },
//    add_products: function(products){
//        this._super(products);
//        if(!products instanceof Array){
//            products = [products]
//        }
//        for(var i = 0, len = products.length; i < len; i++){
//            var prod = products[i]
//            this.product_by_old_barcode[prod.old_barcode] = prod
//        }
//    },
//    get_product_by_old_barcode: function(barcode){
//        if(this.product_by_old_barcode[barcode.code.trim()]){
//            return this.product_by_old_barcode[barcode.code.trim()];
//        } else {
//            return undefined;
//        }
//    },

    _product_search_string: function(product){
    console.log("ZZZZZZZZ")
        var str = product.display_name;
        console.log("self.lot+++++",lot_ids);
        console.log("self.pro+++++++",prod_id);
        if (product.barcode) {
            str += '|' + product.barcode;
        }
        if (product.default_code) {
            str += '|' + product.default_code;
        }
        if (product.description) {
            str += '|' + product.description;
        }
        if (product.description_sale) {
            str += '|' + product.description_sale;
        }
        if (product.old_barcode) {
            str += '|' + product.old_barcode;
        }
        str  = product.id + ':' + str.replace(/:/g,'') + '\n';
        console.log("Strrrrrrr :::",str);
        return str;
    },
});

});