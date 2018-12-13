var commentSource = null;

function randomChoice(arr) {
    return arr[Math.floor(arr.length * Math.random())];
}

var newQuestion = function(data) {
    var comment = null;

    if (Math.random() > 0.5) {
        // reddit
        comment = randomChoice(data['reddit']);
        commentSource = 'reddit';
    } else {
        // 4chan
        comment = randomChoice(data['fourchan']);
        commentSource = '4chan';
    }

    $('#question>blockquote').text(comment);
};

$(document).ready(function() {
    var data = {};

    $.get('comments.txt', function(d) {
        data = JSON.parse(d);
        console.log(data);
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
