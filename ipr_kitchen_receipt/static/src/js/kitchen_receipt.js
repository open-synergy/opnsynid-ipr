openerp.ipr_kitchen_receipt = function(instance){
    var module   = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var _super = module.Order;
    module.Order = module.Order.extend({
        export_as_JSON: function(){
            var json = _super.prototype.export_as_JSON.apply(this,arguments);   
            json.customer = this.get_client_name();
            return json;
        },
        computeChanges: function(categories){
            var res = _super.prototype.computeChanges.apply(this,arguments);
            var json    = this.export_as_JSON();
            var date = new Date();
            locale = "en-us"

            res.customer = json.customer;
            res.date = { 
                year: date.getFullYear(), 
                month: date.getMonth(),
                month_name: date.toLocaleString(locale, { month: "short" }),
                date: date.getDate(),
                day: date.getDay(),
                hour: date.getHours(), 
                minute: date.getMinutes() ,
                isostring: date.toISOString(),
                localestring: date.toLocaleString(),
            };
            return res;
        },
    });
}
