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
            res.customer = json.customer;
            return res;
        },
    });
}
