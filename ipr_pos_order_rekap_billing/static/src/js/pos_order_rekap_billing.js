function print_rekap_billing(instance,module){
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    module.RekapBilling = Backbone.Model.extend({
        get_all_order: function(){
            var details = [];
            var obj_pos_order = new openerp.Model('pos.order');
            var today = new Date();
            var validation_date = new Date(today.setDate(today.getDate())).toISOString();
            obj_pos_order.query(["pos_reference"])
                .filter([['date_order','=',validation_date],['state', 'not in', ['draft', 'cancel']]])
                .first()
                .then(function (orders) {
                    alert(validation_date);
                    if (orders){
                        alert(orders);
                        return {
                            'pos_reference': orders.pos_reference
                        };
                    }else{
                        return {}
                    }
                })
        },
/*        printChanges: function(){
            var printers = this.pos.printers;
            for(var i = 0; i < printers.length; i++){
                var changes = this.computeChanges(printers[i].config.product_categories_ids);
                if ( changes['new'].length > 0 || changes['cancelled'].length > 0){
                    var receipt = QWeb.render('OrderChangeReceipt',{changes:changes, widget:this});
                    printers[i].print(receipt);
                }
            }
        },*/
    })

    module.PosWidget.include({
        build_widgets: function(){
            var self = this;
            this._super();

            if(this.pos.printers.length){
                var rekap_billing = $(QWeb.render('RekapBillingButton'));

                rekap_billing.click(function(){
                    rekap = new module.RekapBilling();
                    rekap.get_all_order();
                });
                rekap_billing.appendTo(this.$('.control-buttons'));
                this.$('.control-buttons').removeClass('oe_hidden');
            }
        },
    });
}
