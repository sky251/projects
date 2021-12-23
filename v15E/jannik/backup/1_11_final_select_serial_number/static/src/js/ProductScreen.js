odoo.define('select_serial_number.ProductLot', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const OrderWidget = require('point_of_sale.OrderWidget');
    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { posbus } = require('point_of_sale.utils');
    const { useListener } = require('web.custom_hooks');
    const { Gui } = require('point_of_sale.Gui');
    const { useState } = owl.hooks;
    var core = require('web.core');
    var _t = core._t
    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');
    const PosComponent = require('point_of_sale.PosComponent');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { parse } = require('web.field_utils');

    models.load_models([{
        model: 'stock.production.lot',
        fields: ['tax_ids', 'id', 'name', 'product_id'],
      loaded: function(self, lots) {
          self.lot_ids = lots;
      },
    }]);

    var super_orderline_model = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        get_all_prices: function(){
            var self = this;
            var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
            console.log("\n\n\n\n\n priceeeeeeeeeeeeeeeeeeeeeee unitttttttttttttttt", price_unit)
            var taxtotal = 0;

            var product =  this.get_product();
            console.log("\n\n\n\n PRODUCTTTTTTTTTTTTTTT ", product, product.selected_lot)
            var taxes =  this.pos.taxes;
            console.log("\n\n\n\n taxes::::::::::::::::::::::::", taxes)
            var taxes_ids = _.filter(product.taxes_id, t => t in this.pos.taxes_by_id);
            console.log("\n\n\n\n taxes_ids::::::::::::::::::::::::", taxes_ids)
            var product_lot_taxes = []
            var lot_taxes = []
            if (['serial', 'lot'].includes(product.tracking) && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)){
                this.pos.taxes.filter(function( item ){
                    if (self.pos.lot_ids){
                        console.log("\n\n\n\n self.pos.lot_ids:::::::::::::::::", self.pos.lot_ids)
                        for (let i = 0; i < self.pos.lot_ids.length; i++){
                            if(product.selected_lot){
                                if(product.selected_lot == self.pos.lot_ids[i]['name']){
                                    console.log("\n\n\n\n lottttttttttttt selected matchedddddd")
                                    lot_taxes.push(self.pos.lot_ids[i]['tax_ids'])
                                }
                                else{
                                    product_lot_taxes = []
                                }
                            }
                        }
                    }
                })
                console.log("\n\n\n\n lot_taxes::::::::::::::::::1111111111::::::", lot_taxes)
                console.log("\n\n\n\n product_lot_taxes:::::::::::::11111111:::::::::::", product_lot_taxes)
                console.log("\n\n\n\n\n @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                console.log("\n\n\n\n\n this.pos.taxes.length:::::::::::::::::::::::",this.pos.taxes.length)
                if (this.pos.taxes.length > 0){
                    this.pos.taxes.filter(function( item ){
                        for (let k = 0; k < lot_taxes.length; k++){
                            for(let m = 0; m < lot_taxes[k].length; m++){
                                if(item['id'] == lot_taxes[k][m]){
                                    product_lot_taxes.push(item)
                                }
                            }
                        }
                    });
                    console.log("\n\n\n\n lot_taxes::::::::::::::::::222222222222222222222::::::", lot_taxes)
                    console.log("\n\n\n\n product_lot_taxes:::::::::::::22222222222222222222222:::::::::::", product_lot_taxes)
                }
                else{
                    product_lot_taxes = []
                }
            }
            var taxdetail = {};
            var product_taxes = [];
            if (['serial', 'lot'].includes(product.tracking) && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)){
                product_taxes = product_lot_taxes;
            }
            else{
                _(taxes_ids).each(function(el){
                    var tax = _.detect(taxes, function(t){
                        return t.id === el;
                    });
                    product_taxes.push.apply(product_taxes, self._map_tax_fiscal_position(tax, self.order));
                });

            }
            console.log("\n\n\n\n PRODUCTCCCCCCCCCCCCCC taxessssssssss uniqueeeeeeeeeeeeeeeeee", product_taxes)
            product_taxes = _.uniq(product_taxes, function(tax) { return tax.id; });
            console.log("\n\n\n\n PRODUCTCCCCCCCCCCCCCC taxessssssssss", product_taxes)

            var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
            console.log("\n\n\n\n all_taxes@@@@@@@@@@@@@@@@@@ taxessssssssss", all_taxes)
            console.log("\n\n\n\n all_taxes_before_discount@@@@@@@@@@@@@@@@@@ taxessssssssss", all_taxes_before_discount)
            var all_taxes_before_discount = this.compute_all(product_taxes, this.get_unit_price(), this.get_quantity(), this.pos.currency.rounding);
            _(all_taxes.taxes).each(function(tax) {
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
            return {
                "priceWithTax": all_taxes.total_included,
                "priceWithoutTax": all_taxes.total_excluded,
                "priceSumTaxVoid": all_taxes.total_void,
                "priceWithTaxBeforeDiscount": all_taxes_before_discount.total_included,
                "tax": taxtotal,
                "taxDetails": taxdetail,
            };
        },
    });

    // var super_orderline_model = models.Orderline.prototype;
    // models.Orderline = models.Orderline.extend({
    //     get_all_prices: function(){
    //         console.log("\N\N\NN\N\N\\NN pricessssssssssssssssssssssssssssssssssss")
    //         var self = this;
    //         var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
    //         var taxtotal = 0;

    //         console.log("\n\n\n\n\n THISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", this, this.pos)
    //         console.log("\n\n\n\n\n THISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSthis.pos.lots_taxesSSSSSSS", this.pos.lots_taxes)
    //         var product =  this.get_product();
    //         console.log("\n\n\nn\n PRODUCTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT:::::::::::::", product)
    //         var taxes =  this.pos.taxes;
    //         var taxes_ids = _.filter(product.taxes_id, t => t in this.pos.taxes_by_id);
    //         var product_lot_taxes = []
    //         var lot_taxes = []
    //         if (['serial', 'lot'].includes(product.tracking) && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)){
    //             this.pos.taxes.filter(function( item ){
    //                 // console.log("\n\n\n\n\n itemmmmmmmmmmmmmmmmmmmmmmmmmm", item)
    //                 // console.log("\n\n\n\n\n self.pos.lot_ids", self.pos.lot_ids)
    //                 // console.log("\n\n\n\n\n this.pos.taxes.length",this.pos.taxes, this.pos.taxes.length)

    //                 if (self.pos.lot_ids){
    //                     for (let i = 0; i < self.pos.lot_ids.length; i++){
    //                         if(product.selected_lot){
    //                             if(product.selected_lot == self.pos.lot_ids[i]['name']){
    //                                 lot_taxes.push(self.pos.lot_ids[i]['tax_ids'])
    //                             }
    //                             else{
    //                                 product_lot_taxes = []
    //                             }
    //                         }
    //                     }
    //                 }
    //             })

    //             if (this.pos.taxes.length > 0){
    //                 this.pos.taxes.filter(function( item ){
    //                     for (let k = 0; k < lot_taxes.length; k++){
    //                         for(let m = 0; m < lot_taxes[k].length; m++){
    //                             if(item['id'] == lot_taxes[k][m]){
    //                                 product_lot_taxes.push(item)
    //                             }
    //                         }
    //                     }
    //                 });
    //             }
    //             else{
    //                 product_lot_taxes = []
    //             }
    //         }
    //         console.log("\n\n\nn\n product_lot_taxes@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", product_lot_taxes)
    //         var taxdetail = {};
    //         var product_taxes = [];
    //         if (['serial', 'lot'].includes(product.tracking) && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)){
    //             product_taxes = product_lot_taxes;
    //         }
    //         else{
    //             _(taxes_ids).each(function(el){
    //                 var tax = _.detect(taxes, function(t){
    //                     return t.id === el;
    //                 });
    //                 product_taxes.push.apply(product_taxes, self._map_tax_fiscal_position(tax, self.order));
    //             });

    //         }
    //         product_taxes = _.uniq(product_taxes, function(tax) { return tax.id; });
    //         console.log("\n\n\n\nn PRODUCTTTTTTTTTTTTTTTTTT TAXESSSSSSSSSSS 1111111111", product_taxes)

    //         var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
    //         console.log("\n\n\n\n all_taxes@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", all_taxes)
    //         var all_taxes_before_discount = this.compute_all(product_taxes, this.get_unit_price(), this.get_quantity(), this.pos.currency.rounding);
    //         _(all_taxes.taxes).each(function(tax) {
    //             taxtotal += tax.amount;
    //             taxdetail[tax.id] = tax.amount;
    //         });
    //         return {
    //             "priceWithTax": all_taxes.total_included,
    //             "priceWithoutTax": all_taxes.total_excluded,
    //             "priceSumTaxVoid": all_taxes.total_void,
    //             "priceWithTaxBeforeDiscount": all_taxes_before_discount.total_included,
    //             "tax": taxtotal,
    //             "taxDetails": taxdetail,
    //         };
    //     },
    // });
    const OrderWidgetCustom = (OrderWidget) =>
    class extends OrderWidget {
        async _editPackLotLines(event) {
            console.log("\n\n\n\nn EDITING:::::::::::::::::::::::::::::::::", event, )
            console.log("\n\n\n\nn EDITING::::::::::::::::event.detail.orderline:::::::::::::::::", event.detail.orderline )
            console.log("\n\n\n\nn EDITING::::::::::::::::::::::::::::event.detail.orderline.product:::::", event.detail.orderline.product )
            const orderline = event.detail.orderline;
            console.log("\n\n\n\n\n ORDERLINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", orderline, orderline.product)
            const isAllowOnlyOneLot = orderline.product.isAllowOnlyOneLot();
            const packLotLinesToEdit = orderline.getPackLotLinesToEdit(isAllowOnlyOneLot);
            const { confirmed, payload } = await this.showPopup('EditListPopup', {
                title: this.env._t('Lot/Serial Number(s) Required'),
                isSingleItem: isAllowOnlyOneLot,
                array: packLotLinesToEdit,
            });
            console.log("\n\n\n\n\n UPDATEEEEEEEEEEEEEEEEEEEEEEEEEE LOTTTTTTTTTTTTTTTTTTTTTTTTTTTT", confirmed, payload)
  /*          if (confirmed) {
                // Segregate the old and new packlot lines
                const data = await this._check_lot_number(product, payload);
                console.log("\n\n\n\n data, msg@@@@@@@@@@@@@", data)
                if (data){
                    const modifiedPackLotLines = Object.fromEntries(
                        payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
                    );
                    const newPackLotLines = payload.newArray
                        .filter(item => !item.id)
                        .map(item => ({ lot_name: item.text }));

                    orderline.setPackLotLines({ modifiedPackLotLines, newPackLotLines });
                } else {
                    this.order.select_orderline(event.detail.orderline);
                }
            } else {
                // We don't proceed on adding product.
                return;
            }*/
            if (confirmed) {
                // Segregate the old and new packlot lines
                orderline.product.selected_lot = payload.newArray.filter(item => item.id)[0]['text']
                const data = await this._check_lot_number(orderline.product['id'], payload);
                console.log("\n\n\n\n data, msg@@@@@@@@@@@@@", data)
                if (data){
                    const modifiedPackLotLines = Object.fromEntries(
                        payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
                    );
                    const newPackLotLines = payload.newArray
                        .filter(item => !item.id)
                        .map(item => ({ lot_name: item.text }));

                    orderline.setPackLotLines({ modifiedPackLotLines, newPackLotLines });
                }
            }
            this.order.select_orderline(event.detail.orderline);
        }
        async _check_lot_number(product, payload) {
            console.log("\n\n\n\n\n\n UPDATEEEEEEEEEEEEENEWWWWWWWWWWWWWWWWWWWWWW functionnnnnnnnnnnnnn called###########", product, payload)
            let data, msg;
            const serial_lot_name = payload.newArray.filter(item => item.id)
            console.log("\n\n\n serial_lot_name@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", serial_lot_name, this)
            console.log("\n\n\n serial_lot_name@@@@@@@@@@@@@@@@@@@@@@@@@@@@@wwwwwwwwww", serial_lot_name[0]['text'])
            var self = this
            console.log("\n\n\nn  product['id']],[serial_lot_name[0]['text']", product['id'],serial_lot_name[0]['text'])
            if (product && serial_lot_name[0]['text']) {
                console.log("\n\n\n 123333333333333333333333333333333333",)
                return rpc.query({
                    model : "stock.production.lot",
                    method : "get_lot_taxes",
                    args : [[],[product],[serial_lot_name[0]['text']]],
                }).then(function(data){
                    console.log("\n\n\n dataaaaaaaaaaaaaaaaaaaaaaaaaaaaqqqqqqqqqqq", data, this, self)
                    if(data[0]['msg']) {
                        self.showPopup('ErrorPopup', {
                            title: self.env._t('Invalid Action'),
                            body: self.env._t(data[0]['msg']),
                        });
                        return;
                    }
                    else{
                        console.log("\n\n\n\n nooooo error msg::::::", data)
                        window.lots_taxes = data
                        self.env.pos['lots_taxes'] = data
                        return data;
                    }
                });
            }

        }
    }

    const PosCustomLotPopUp = (ProductScreen) =>
    class extends ProductScreen {
        async _getAddProductOptions(product) {
            let price_extra = 0.0;
            let draftPackLotLines, weight, description, packLotLinesToEdit;

            if (this.env.pos.config.product_configurator && _.some(product.attribute_line_ids, (id) => id in this.env.pos.attributes_by_ptal_id)) {
                let attributes = _.map(product.attribute_line_ids, (id) => this.env.pos.attributes_by_ptal_id[id])
                                  .filter((attr) => attr !== undefined);
                let { confirmed, payload } = await this.showPopup('ProductConfiguratorPopup', {
                    product: product,
                    attributes: attributes,
                });

                if (confirmed) {
                    description = payload.selected_attributes.join(', ');
                    price_extra += payload.price_extra;
                } else {
                    return;
                }
            }

            // Gather lot information if required.
            if (['serial', 'lot'].includes(product.tracking) && (this.env.pos.picking_type.use_create_lots || this.env.pos.picking_type.use_existing_lots)) {
                const isAllowOnlyOneLot = product.isAllowOnlyOneLot();
                if (isAllowOnlyOneLot) {
                    packLotLinesToEdit = [];
                } else {
                    const orderline = this.currentOrder
                        .get_orderlines()
                        .filter(line => !line.get_discount())
                        .find(line => line.product.id === product.id);
                    if (orderline) {
                        packLotLinesToEdit = orderline.getPackLotLinesToEdit();
                    } else {
                        packLotLinesToEdit = [];
                    }
                }
                const { confirmed, payload } = await this.showPopup('EditListPopup', {
                    title: this.env._t('Lot/Serial Number(s) Required'),
                    isSingleItem: isAllowOnlyOneLot,
                    array: packLotLinesToEdit,
                });
                if (confirmed) {
                    // Segregate the old and new packlot lines
                    product.selected_lot = payload.newArray.filter(item => !item.id)[0]['text']
                    const data = await this._check_lot_number(product, payload);
                    console.log("\n\n\n\n data, msg@@@@@@@@@@@@@", data)
                    if (data){
                        const modifiedPackLotLines = Object.fromEntries(
                            payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
                        );
                        const newPackLotLines = payload.newArray
                            .filter(item => !item.id)
                            .map(item => ({ lot_name: item.text }));

                        draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
                    } else {
                        // We don't proceed on adding product.
                        return;
                    }
                } else {
                    // We don't proceed on adding product.
                    return;
                }
            }

            // Take the weight if necessary.
            if (product.to_weight && this.env.pos.config.iface_electronic_scale) {
                // Show the ScaleScreen to weigh the product.
                if (this.isScaleAvailable) {
                    const { confirmed, payload } = await this.showTempScreen('ScaleScreen', {
                        product,
                    });
                    if (confirmed) {
                        weight = payload.weight;
                    } else {
                        // do not add the product;
                        return;
                    }
                } else {
                    await this._onScaleNotAvailable();
                }
            }

            return { draftPackLotLines, quantity: weight, description, price_extra };
        }
        async _check_lot_number(product, payload) {
            console.log("\n\n\n\n\n\n NEWWWWWWWWWWWWWWWWWWWWWW functionnnnnnnnnnnnnn called###########", product, payload)
            let data, msg;
            const serial_lot_name = payload.newArray
                .filter(item => !item.id)
            console.log("\n\n\n serial_lot_name@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", serial_lot_name, this)
            console.log("\n\n\n serial_lot_name@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", serial_lot_name[0]['text'])
            var self = this
            console.log("\n\n\nn  product['id']],[serial_lot_name[0]['text']", product['id'],serial_lot_name[0]['text'])
            if (product['id'] && serial_lot_name[0]['text']) {
                console.log("\n\n\n 123333333333333333333333333333333333",)
                return rpc.query({
                    model : "stock.production.lot",
                    method : "get_lot_taxes",
                    args : [[],[product['id']],[serial_lot_name[0]['text']]],
                }).then(function(data){
                    console.log("\n\n\n dataaaaaaaaaaaaaaaaaaaaaaaaaaaaqqqqqqqqqqq", data, this, self)
                    if(data[0]['msg']) {
                        self.showPopup('ErrorPopup', {
                            title: self.env._t('Invalid Action'),
                            body: self.env._t(data[0]['msg']),
                        });
                        return;
                    }
                    else{
                        console.log("\n\n\n\n nooooo error msg::::::", data)
                        window.lots_taxes = data
                        self.env.pos['lots_taxes'] = data
                        return data;
                    }
                });
            }

        }
       }
    Registries.Component.extend(ProductScreen, PosCustomLotPopUp);
    Registries.Component.extend(OrderWidget, OrderWidgetCustom);
    return PosCustomLotPopUp,OrderWidgetCustom;
});
