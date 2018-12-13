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

$(document).ready(function() {
    var data = {};

    $.get('comments.txt', function(d) {
        data = JSON.parse(d);
        updateComments(data);

        newQuestion(data);
    })

    $('#question button[name="reddit"]').click(function(e) {
        if (commentSource === 'reddit') {
            alert('yeah. okay. you win. whatever');
        } else {
            alert('wrong.');
        }

        newQuestion(data);
    });

    $('#question button[name="4chan"]').click(function(e) {
        if (commentSource === 'reddit') {
            alert('wrong.');
        } else {
            alert('yeah. okay. you win. whatever');
        }

        newQuestion(data);
    });
});
