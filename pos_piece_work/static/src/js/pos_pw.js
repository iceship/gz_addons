
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
    
};
