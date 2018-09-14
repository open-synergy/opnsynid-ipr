function print_rekap_billing(instance,module){
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        self = this;
        for (var i = 0 ; i < this.models.length; i++){
            if (this.models[i].model == 'restaurant.printer'){
                if (this.models[i].fields.indexOf('print_rekap_bill') == -1) {
                    this.models[i].fields.push('print_rekap_bill');
                }
            }
            if (this.models[i].model == 'pos.order'){
                if (this.models[i].fields.indexOf('amount_total') == -1) {
                    this.models[i].fields.push('amount_total');
                }
            }
            if (this.models[i].model == 'stock.warehouse'){
                if (this.models[i].fields.indexOf('name') == -1) {
                    this.models[i].fields.push('name');
                }
            }
        }
        return _initialize_.call(this, session, attributes);
    };

    module.PosWidget = module.PosWidget.extend({
        computeDetails: function(order_list){
            details = [];
            var today = new Date();
            var months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"];
            format_date = today.getDate() + '-' + months[today.getMonth()] + '-' + today.getFullYear();
            order_list.sort(function(a, b){
                return a.id - b.id

            });
            console.log(order_list);
            for(var i = 0; i < order_list.length; i++){
                lines = [];
                if (order_list[i]){
                    order_lines = order_list[i].lines
                    for(var y = 0; y < order_lines.length; y++){
                        if (order_lines[y]){
                            var lines_data = this.pos.db.line_by_id[order_lines[y]];
                            lines.push({
                                'qty': lines_data.qty,
                                'price_subtotal_incl': lines_data.price_subtotal_incl,
                                'product_name': this.pos.db.get_product_by_id(lines_data.product_id[0]).display_name
                            })
                        }
                    }
                    details.push({
                        'pos_reference': order_list[i].pos_reference,
                        'lines': lines,
                        'amount_total': order_list[i].amount_total,
                    });
                }
            }
            return {
                'data': details,
                'warehouse': this.pos.warehouse.name || '',
                'tanggal': format_date,
            };
            
        },
        print_rekap: function(order_list) {
            var printers = this.pos.printers;
            for(var i = 0; i < printers.length; i++){
                if (printers[i].config.print_rekap_bill){
                    var details = this.computeDetails(order_list);
                    var receipt = QWeb.render('RekapBill',{details:details, widget:this});
                    printers[i].print(receipt);
                }
            }
        },
        build_widgets: function(){
            var self = this;
            this._super();

            if(this.pos.printers.length){
                var rekap_billing = $(QWeb.render('RekapBillingButton'));

                rekap_billing.click(function(){
                    var order_list = self.pos.db.pos_all_orders;
                    self.print_rekap(order_list);
                });
                rekap_billing.appendTo(this.$('.control-buttons'));
                this.$('.control-buttons').removeClass('oe_hidden');
            }
        },
    });
}
