
openerp.pos_piece_work = function(instance) {

    var _t = instance.web._t, _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    $('<link rel="stylesheet" href="/pos_piece_work/static/src/css/pos_pw.css"/>').appendTo($("head"));
    
    instance.point_of_sale.PosDB.include({
        get_product_by_category: function(category_id) {
            if (category_id == 0) {
                return [];
            } else {
                return this._super.apply(this, arguments);
            }
        },
    });
    
    instance.point_of_sale.PaypadButtonWidget.include({
        renderElement: function() {
            var self = this;
            this._super.apply(this, arguments);
            this.$el.unbind("click");
            this.$el.click(function(){
                if (self.pos.get('selectedOrder').get('screen') === 'receipt'){  //TODO Why ?
                    console.warn('TODO should not get there...?');
                    return;
                }
                self.pos.get('selectedOrder').addPaymentline(self.cashregister);
                
                //self.pos_widget.screen_selector.set_current_screen('payment');
                var currentOrder = self.pos.get('selectedOrder');
                self.pos.push_order(currentOrder);
                self.pos_widget.screen_selector.set_current_screen("receipt");
            });
        },
    });

    instance.point_of_sale.ReceiptScreenWidget.include({
        print: function() {
            this.pos.get('selectedOrder')._printed = true;
            // window.print();
        },
    });
};
