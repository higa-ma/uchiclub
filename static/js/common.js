

$(function(){
    $('.answer1-input').on('click', function() {
      if ($(this).prop('checked')){
        // 一旦全てをクリアして再チェックする
        $('.answer1-input').prop('checked', false);
        $(this).prop('checked', true);
      }
    });

    $('.answer2-input').on('click', function() {
        if ($(this).prop('checked')){
          // 一旦全てをクリアして再チェックする
          $('.answer2-input').prop('checked', false);
          $(this).prop('checked', true);
        }
      });


  });

