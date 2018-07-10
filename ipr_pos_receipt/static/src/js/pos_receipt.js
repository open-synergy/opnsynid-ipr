openerp.ipr_pos_receipt = function(instance){
    var module   = instance.point_of_sale;
    var round_pr = instance.web.round_precision
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    module.PosModel.prototype.models.push({
        model: "stock.picking.type",
        fields: ["warehouse_id"],
        ids: function(self){
            return [self.config.picking_type_id[0]];
        },
        loaded: function(self, picking_type){
            self.picking_type = picking_type[0];
        },
    });

    module.PosModel.prototype.models.push({
        model: "stock.warehouse",
        fields: ["partner_id"],
        domain: function(self){ 
            return [['id','=', self.picking_type.warehouse_id[0]]];
        },
        loaded: function(self, warehouse){
            self.warehouse = warehouse[0];
        },
    });

    module.PosModel.prototype.models.push({
        model: "res.partner",
        fields: [],
        domain: function(self){
            if (self.warehouse || self.warehouse.partner_id){
                return [['id','=', self.warehouse.partner_id[0]]];
            }
            else{
                return [];
            }
        },
        loaded: function(self, shop_addresses){
            if (self.warehouse || self.warehouse.partner_id){
                self.shop_address = shop_addresses[0];
            }
            else{
                return [];
            }
        },
    });

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
            var shop_address = this.pos.shop_address;

            locale = "en-us"
            order['config_name'] = this.pos.config.name || '';
            order['date']['month_name'] = date.toLocaleString(locale, { month: "short" });
            order['date']['seconds'] = date.getSeconds();
            order['table'] = this.get_table();
            order['wk_get_discount'] = this.wk_get_discount();
            order['get_discount_value'] = this.get_discount_value();
            order['picking_type_id'] = this.pos.config.picking_type_id || '';
            order['shop_address'] = {
                contact_adress : shop_address.contact_adress,
                phone : shop_address.phone,
                vat : shop_address.vat,
                email : shop_address.email,
                website : shop_address.website,
            }
            return order;
        },
    });
}
