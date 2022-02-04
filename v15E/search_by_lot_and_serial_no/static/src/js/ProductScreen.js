odoo.define('search_by_lot_and_serial_no.ProductScreen', function(require) {
    'use strict';
    var core = require('web.core');
    var utils = require('web.utils');
    var PosDB = require('web.utils');
    var models = require('point_of_sale.models');
    var DB = require('point_of_sale.DB');
    var rpc = require('web.rpc');
    const ProductScreen = require('point_of_sale.ProductScreen');
    var lot_ids;
    var prod_id;

    models.load_models([{
        model: 'stock.production.lot',
        fields: ['id', 'name', 'product_id'],
        loaded: function(self, lots) {
        self.lot_ids = lots
      },
    }]);
    models.load_fields("product.product", "lot_ids");

    DB.include({
    init: function( options ){
        this._super(options);
        var self = this
        this.product_lot = {}
    },

    _product_search_string: function(product){
        var str = product.display_name;
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
        if (product.lot_ids) {
            str += '|' + product.lot_ids;
        }
        str = product.id + ':' + str.replace(/:/g,'') + '\n';
        return str;
    },

    });

});