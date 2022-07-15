$(function () {
    var IMP = window.IMP; //아임포트 매뉴얼대로
    IMP.init('imp40292613'); //가맹점 코드
    //order-form에 submit을 했을 때 일어날 일 수행
    $('.order-form').on('submit', function (e) {
        var amount =parseInt($('.order-form input[name="amount"]').val().replace('원', ''));
        //동작안하는 코드. 카트, 무통장
        var type = $('.order-form input[name="type"]:checked').val();
        // 폼 데이터를 기준으로 주문 생성
        var order_id = AjaxCreateOrder(e);
        if (order_id == false) { //주문을 제대로 생성했을 때 만들어라
            alert('주문 생성 실패\n다시 시도해주세요.');
            return false;
        }

        // 결제 정보 생성. transaction을 이 시점에 만들어중
        var merchant_id = AjaxStoreTransaction(e, order_id, amount, type);

        // 결제 정보가 만들어졌으면 iamport로 실제 결제 시도
        if (merchant_id !== '') {
            IMP.request_pay({ //requestpay에서 값 2개 넘김
                merchant_uid: merchant_id,
                name: 'E-Shop product',
                buyer_name:$('input[name="name"]').val(),
                buyer_email:$('input[name="email"]').val(),
                amount: amount
            }, function (rsp) { //request 정보
                if (rsp.success) {
                    var msg = '결제가 완료되었습니다.';
                    msg += '고유ID : ' + rsp.imp_uid;
                    msg += '상점 거래ID : ' + rsp.merchant_uid;
                    msg += '결제 금액 : ' + rsp.paid_amount;
                    msg += '카드 승인번호 : ' + rsp.apply_num;
                    // 결제가 완료되었으면 비교해서 디비에 반영
                    ImpTransaction(e, order_id, rsp.merchant_uid, rsp.imp_uid, rsp.paid_amount);
                } else {
                    var msg = '결제에 실패하였습니다.';
                    msg += '에러내용 : ' + rsp.error_msg;
                    console.log(msg);
                }
            });
        }
        return false;
    });
});

// 폼 데이터를 기준으로 주문 생성. ordercreateView를 작동시킴
function AjaxCreateOrder(e) {
    e.preventDefault(); //폼이 submit되는 것을 막아줌
    var order_id = '';
    var request = $.ajax({ //order생성하는 뷰 호출
        method: "POST",
        url: order_create_url,
        async: false, //동기로 진행시킴
        data: $('.order-form').serialize() //데이터를 가져와서 넘겨주도록 함
    });
    request.done(function (data) { //request 응답이 온 후의 대처
        if (data.order_id) { //data order_id 뷰의 ordercreateajaxview에서 할당해줌
            order_id = data.order_id;
        }
    });
    request.fail(function (jqXHR, textStatus) { //문제가 생겼을 때 응답방법
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (jqXHR.status == 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다. 다시 시도해주세요.");
        }
    });
    return order_id;
}

// 결제 정보 생성
function AjaxStoreTransaction(e, order_id, amount, type) {
    e.preventDefault();
    var merchant_id = '';
    var request = $.ajax({
        method: "POST",
        url: order_checkout_url, //create.html의 자바스크립트에 시그널 보냄
        async: false,
        data: {
            order_id : order_id,
            amount: amount,
            type: type,
            csrfmiddlewaretoken: csrf_token,
        }
    });
    request.done(function (data) {
        if (data.works) {
            merchant_id = data.merchant_id;
        }
    });
    request.fail(function (jqXHR, textStatus) {
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (jqXHR.status == 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다. 다시 시도해주세요.");
        }
    });
    return merchant_id;
}

// iamport에 결제 정보가 있는지 확인 후 결제 완료 페이지로 이동
//validation 수행
//위의 imptransaction에서 다시 한 번 더 물어보기
function ImpTransaction(e, order_id,merchant_id, imp_id, amount) {
    e.preventDefault();
    var request = $.ajax({
        method: "POST",
        url: order_validation_url,
        async: false,
        data: {
            order_id:order_id,
            merchant_id: merchant_id,
            imp_id: imp_id, //변수명과 실제 객체 값 넣어줌
            amount: amount,
            csrfmiddlewaretoken: csrf_token
        }
    });
    request.done(function (data) {
        if (data.works) { //잘 끝났으면 페이지 이동시키기. order_complete view로 넘기기
            $(location).attr('href', location.origin+order_complete_url+'?order_id='+order_id)
        }
    });
    request.fail(function (jqXHR, textStatus) {
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (jqXHR.status == 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다. 다시 시도해주세요.");
        }
    });
}