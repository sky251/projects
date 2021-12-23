odoo.define('web_widget_float_hhmmss.float_hhmmss', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;

    var ListView = require('web.ListView');
    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');

//    ListView.Column.include({
//        _format: function (row_data, options) {
//            var value = row_data[this.id].value;
//            if (typeof value === 'number' && isNaN(value)) {
//                value = false;
//            }
//            var l10n = _t.database.parameters;
//            var pattern = '%02d:%02d:%02d';
//            if (value < 0) {
//                value = Math.abs(value);
//                pattern = '-' + pattern;
//            }
//            hours = Math.floor(value / 3600);
//            value %= 3600;
//            minutes = Math.floor(value / 60);
//            seconds = value % 60;
//            value = _t.str.sprintf(pattern, hours, minutes, seconds);
//            return value;
//         },
//    });
//
//    core.list_widget_registry.add('float_hhmmss', ListView.Column);

    var FieldHHMMSS = basic_fields.FieldFloat.extend({
        _parse_value: function(val, def) {
            debugger;
            var factor = 1;
            if (val[0] === '-') {
                val = val.slice(1);
                factor = -1;
            }
            var float_time_pair = val.split(":");
            if (float_time_pair.length != 3)
                return factor * instance.web.parse_value(val, {type: "float"});
            var hours = instance.web.parse_value(float_time_pair[0], {type: "integer"});
            var minutes = instance.web.parse_value(float_time_pair[1], {type: "integer"});
            var seconds = instance.web.parse_value(float_time_pair[2], {type: "integer"});
            return factor * (hours * 3600 + minutes * 60 + seconds );
        },
        _format_value: function(value, value_if_empty) {
            debugger;
            // If NaN value, display as with a `false` (empty cell)
            if (typeof value === 'number' && isNaN(value)) {
                value = false;
            }
            //noinspection FallthroughInSwitchStatementJS
            switch (value) {
                case '':
                    if (this.type === 'char' || this.type === 'text') {
                        return '';
                    }
                    console.warn('Field', this, 'had an empty string as value, treating as false...');
                    return value_if_empty === undefined ?  '' : value_if_empty;
                case false:
                case undefined:
                case Infinity:
                case -Infinity:
                    return value_if_empty === undefined ?  '' : value_if_empty;
            }
            var l10n = _t.database.parameters;
            var pattern = '%02d:%02d:%02d';
            if (value < 0) {
                value = Math.abs(value);
                pattern = '-' + pattern;
            }
            hours = Math.floor(value / 3600);
            value %= 3600;
            minutes = Math.floor(value / 60);
            seconds = value % 60;
            return _t.str.sprintf(pattern, hours, minutes, seconds);
        },
    });

    field_registry.add('float_hhmmss', FieldHHMMSS);

    return FieldHHMMSS;
});
