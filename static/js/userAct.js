
var log = function () {
    console.log(arguments);
};

// user API
var user = {

};

user.ajax = function(url, method, form, success, error) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('user post success', url, r);
            success(r);
        },
        error: function (err) {
            r = {
                success: false,
                data: err
            };
            log('user post err', url, err);
            error(r);
        }
    };
    if(method === 'post') {
        var data = JSON.stringify(form);
        log('data, ', data)
        request.data = data;
    }
    $.ajax(request);
};

user.get = function(url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response, response);
};

user.post = function(url, form, success, error) {
    var method = 'post';
    this.ajax(url, method, form, success, error);
};

var user_act = function (user_id) {
    var status = $('a#status').text();
    var numberFollows = $('#id-badge-follows');
    var numberFans = $('#id-badge-fans');
    var count;
    if (status == '关注') {
        var url = '/api/follow';
        var success = function () {
            log('status success, ');
            $('a#status').text('取消关注');
            count = +numberFans.text();
            numberFans.text(count+1);
        };
    }else if (status =='取消关注') 
        {
        url = '/api/unfollow';
        var success = function () {
            log('status error, ');
            $('a#status').text('关注');
            count = +numberFans.text();
            numberFans.text(count-1);
        }
    }
    var form = {
        id: user_id
    };
    var error = function (err) {
        log('reg, ', err);
    };
    user.post(url, form, success, error)
};
