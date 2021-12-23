openerp.web_widget_float_hhmmss = function (instance) {
    var _t = instance.web._t;
    instance.web.list.columns.add('field.float_hhmmss', 'instance.web.list.FloatHHMMSS');
    instance.web.list.FloatHHMMSS = instance.web.list.Char.extend({
        _format: function (row_data, options) {
            var value = row_data[this.id].value;
            if (typeof value === 'number' && isNaN(value)) {
                value = false;
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
            value = _.str.sprintf(pattern, hours, minutes, seconds);
            return value;
         },
    });
    instance.web.form.widgets.add('float_hhmmss', 'openerp.web_widget_float_hhmmss.WebFloatHHMMSS');
    instance.web_widget_float_hhmmss.WebFloatHHMMSS = instance.web.form.FieldFloat.extend({
        parse_value: function(val, def) {
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
        format_value: function(value, value_if_empty) {
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
            return _.str.sprintf(pattern, hours, minutes, seconds);
        },
    });

};
