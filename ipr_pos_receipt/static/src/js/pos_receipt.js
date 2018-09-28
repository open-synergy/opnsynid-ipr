openerp.ipr_pos_receipt = function(instance){
    var module   = instance.point_of_sale;
    var round_pr = instance.web.round_precision
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var moduleOrderParent = module.Order;
    module.Order = module.Order.extend({
        get_discount_value:function(){
            var wkdiscount_info=this.get('wkdiscount_info')
            if (wkdiscount_info == undefined){               
                return "";
            }
            else{
               
                if(wkdiscount_info.discount_type=='percent')
                {   
                    return wkdiscount_info.discount_value+" %";
                    
                }
               else{
                   return wkdiscount_info.discount_value;
               }
            }
        },
        export_for_printing: function(attributes){
            var order = moduleOrderParent.prototype.export_for_printing.apply(this, arguments);
            var date = new Date();
            locale = "en-us"
            order['config_name'] = this.pos.config.name || '';
            order['date']['month_name'] = date.toLocaleString(locale, { month: "short" });
            order['date']['seconds'] = date.getSeconds();
            order['table'] = this.get_table();
            order['wk_get_discount'] = this.wk_get_discount();
            order['get_discount_value'] = this.get_discount_value();
            return order;
        },
    });
}
