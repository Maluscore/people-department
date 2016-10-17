
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

var show_weibo = function (userId) {
    var url = '/user/profile/' + userId;
    var form = {
        id: userId
    };
    var success = function (r) {
        if (r.success) {
            log(r.message);
            // $('#id-div-insert').css('display', 'none');
            // var tweets_list = (`<div class="pp-div-tweets-list"></div>`);
            // $('.pp-div-release').after(tweets_list);
            // for (var i=0; i<r.data.length; i++) {
            //     var tweet_item = (`
            //             <div class="pp-panel pp-flex-row" data-id="${r.data[i].id}">
            //                 <div class="pp-avatar pp-avatar-config">
            //                     <img class="pp-avatar-me" src="/static/img/head-min.jpg">
            //                 </div>
            //                 <div class="pp-main flex-1">
            //                     <div class="pp-main-header">
            //                         <strong class="pp-full-name">${r.data[i].sender_name}</strong>
            //                         <span class="pp-timestamp" data-time=${r.data[i].created_time}></span>
            //                     </div>
            //                     <div class="pp-main-content">
            //                         <p class="pp-weibo-text">${r.data[i].content}</p>
            //                     </div>
            //                    <!-- <div class="pp-main-pic">
            //                         <img class="pp-weibo-pic" src="/static/img/main-pic.jpg">
            //                     </div> -->
            //                     <div class="pp-main-footer">
            //                         <a class="btn icon-share-alt" title="转发"> 0</a>
            //                         <a class="btn icon-comment" title="评论"> ${r.data[i].com_count}</a>
            //                         <a class="btn icon-thumbs-up" title="赞"> ${r.data[i].likes_count}</a>
            //                         <a class="btn icon-cog" title="设置"></a>
            //                     </div>
            //                 </div>
            //             </div>`);
            //     $('.pp-div-tweets-list').append(tweet_item);
            // }
            window.location.href = r.next;
        } else {
            log('操作失败')
        }
    };
    var error = function (err) {
        log('reg, ', err);
    };
    user.post(url, form, success, error)
};
