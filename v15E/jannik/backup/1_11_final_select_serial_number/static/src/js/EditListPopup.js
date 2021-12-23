odoo.define('select_serial_number.EditListPopup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    const EditListPopup = require('point_of_sale.EditListPopup');
    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { posbus } = require('point_of_sale.utils');
    const { useListener } = require('web.custom_hooks');
    const { Gui } = require('point_of_sale.Gui');
    const { useAutoFocusToLast } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;
    var core = require('web.core');
    var _t = core._t
    var rpc = require('web.rpc');
    var lot_values, product_lots;
    lot_values = rpc.query({
        model : "stock.production.lot",
        method : "search_read",
        args : [[], ['id', 'name','product_id']],
    }).then(function(data){
        console.log(data);
        product_lots = data
    });

    const PosCustomLotPopUp = (EditListPopup) =>
    class extends EditListPopup {
        constructor() {
            super(...arguments);
            this._id = 0;
            this.lots=product_lots;
            useAutoFocusToLast();
            }


        selectItem(itemId) {
            this.lots.selectedId = itemId;
            this.confirm();
        }
         _nextId() {
            return this._id++;
        }
        _emptyItem() {
            return {
                text: '',
                _id: this._nextId(),
            };
        }
        _initialize(array) {
            // If no array is provided, we initialize with one empty item.
            if (array.length === 0) return [this._emptyItem()];
            // Put _id for each item. It will serve as unique identifier of each item.
            return array.map((item) => Object.assign({}, { _id: this._nextId() }, typeof item === 'object'? item: { 'text': item}));
        }
        removeItem(event) {
            const itemToRemove = event.detail;
            this.lots.splice(
                this.lots.findIndex(item => item._id == itemToRemove._id),
                1
            );
            // We keep a minimum of one empty item in the popup.
            if (this.lots.length === 0) {
                this.lots.push(this._emptyItem());
            }
        }
        createNewItem() {
            if (this.props.isSingleItem) return;
            this.lots.push(this._emptyItem());
        }
        /**
         * We send as payload of the response the selected item.
         *
         * @override
         */
        // getPayload() {
        //     const selected = this.lots.selectedId;
        //     return selected && selected.item;
        // }
        getPayload() {
            return {
                newArray: this.lots
                    .filter((item) => item.name.trim() !== '')
                    .map((item) => Object.assign({}, item)),
            };
        }
        }
    EditListPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        isSingleItem: false,
    };
            
    Registries.Component.extend(EditListPopup, PosCustomLotPopUp);
    return PosCustomLotPopUp;
});
