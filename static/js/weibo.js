
// log
var log = function () {
    console.log(arguments);
};

// long time ago
    var longTimeAgo = function(timeStamp) {
      var timeAgo = function(time, ago) {
        return Math.round(time) + ago;
      };
      log('开始处理时间');
      $(timeStamp).each(function(i, e){
        var past = parseInt(e.dataset.time);
        var now = Math.round(new Date().getTime() / 1000);
        var seconds = now - past;
        var ago = seconds / 60;
        // log('time ago', e, past, now, ago);
        var oneHour = 60;
        var oneDay = oneHour * 24;
        // var oneWeek = oneDay * 7;
        var oneMonth = oneDay * 30;
        var oneYear = oneMonth * 12;
        var s = '';
        if(seconds < 60) {
            s = timeAgo(seconds, '秒前')
        } else if (ago < oneHour) {
            s = timeAgo(ago, '分钟前');
        } else if (ago < oneDay) {
            s = timeAgo(ago/oneHour, '小时前');
        } else if (ago < oneMonth) {
            s = timeAgo(ago / oneDay, '天前');
        } else if (ago < oneYear) {
            s = timeAgo(ago / oneMonth, '月前');
        }
        $(e).text(s);
      });
    };

// form 可以对一类的值进行处理与获取
var formFromKeys = function(keys, prefix) {
    var form = {};
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        if (value.length < 1) {
            // alert('字段不能为空');
            break;
        }
        $('#' + tagid).val('');
        form[key] = value;
    }
    return form;
};

// weibo API
var weibo = {};

var tweetForm = function () {
    var keys = [
        'content',
    ];
    var tweetPrefix = 'id-textarea-';
    var form = formFromKeys(keys, tweetPrefix);
    return form;
};

weibo.post = function(url, form, success, error) {
    var data = JSON.stringify(form);
    var request = {
        url: url,
        type: 'post',
        contentType: 'application/json',
        data: data,
        success: function (r) {
            log('post success', url, r);
            success(r);
        },
        error: function (err) {
            log('post err', url, err);
            error(err);
        }
    };
    $.ajax(request);
};

weibo.register = function(form, success, error) {
    var url = '/register';
    this.post(url, form, success, error);
};

weibo.login = function(form, success, error) {
    var url = '/login';
    this.post(url, form, success, error);
};
