var commentSource = null;
var commentTotal = 0;

function randomIdx(arr) {
    return Math.floor(arr.length * Math.random());
}

var updateComments = function(data) {
    commentTotal =
        data['reddit'].length + data['fourchan'].length;
    $('#commentTotal').text(commentTotal);
};

var newQuestion = function(data) {
    var idx = null;
    var comment = null;

    if (Math.random() > 0.5) {
        // reddit
        idx = randomIdx(data['reddit']);
        comment = data['reddit'][idx];
        commentSource = 'reddit';
        data['reddit'].splice(idx, 1);
    } else {
        // 4chan
        idx = randomIdx(data['fourchan']);
        comment = data['fourchan'][idx];
        commentSource = '4chan';
        data['fourchan'].splice(idx, 1);
    }

    $('#question>blockquote').text(comment);
    updateComments(data);
};

var onReddit = function(data) {
    if (commentSource === 'reddit') {
        alert('yeah. okay. you win. whatever. it was reddit.');
    } else {
        alert('wrong. 4chan.');
    }

    newQuestion(data);
};
var onFourchan = function(data) {
    if (commentSource === 'reddit') {
        alert('wrong. reddit.');
    } else {
        alert('yeah. okay. you win. whatever. it was 4chan.');
    }

    newQuestion(data);
};

$(document).ready(function() {
    var data = {};

    $.ajax({
        method: 'get',
        url: 'comments.json',
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        },
        cache: false,
        success: function(d) {
            data = d;
            updateComments(d);
            newQuestion(d);
        }
    });

    $('#question button[name="reddit"]').click(function(e) {
        onReddit(data);
    });

    $('#question button[name="4chan"]').click(function(e) {
        onFourchan(data);
    });

    document.addEventListener('keydown', function(e) {
        if (event.ctrlKey || event.metaKey) {
            return;
        }

        if (e.key.toLowerCase() === 'r') {
            onReddit(data);
        } else if (
            e.key.toLowerCase() === 'f' ||
                e.key.toLowerCase() === '4'
        ) {
            onFourchan(data);
        }
    });
});
