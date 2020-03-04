$(document).ready(function () {


     var x=0;
     var y=0;
     var city="ini";
     var pro="ini";

     let BMap = window.BMap;
       let geolocation = new BMap.Geolocation();
           geolocation.enableSDKLocation(); //允许SDK辅助
           geolocation.getCurrentPosition(function (r) {
           console.log("huoqu")
         if(this.getStatus() == 0){
             x=r.point.lng;
             y=r.point.lat;
             city=r.address.city;
             pro=r.address.province;
              console.log(r);
         }else{
            x=-1;
            y=-1;
            city="no";
            pro="np"
              console.log("wrong")
              }
         })


    $(document).ajaxError(function (event, request) {
        var message = null;
        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            var IS_JSON = true;
            try {
                var data = JSON.parse(request.responseText);
            }
            catch (err) {
                IS_JSON = false;
            }

            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        M.toast({html: message});
    });

     
    

    $(document).on('click', '#confirm_student', function(){
       console.log("to student")
       window.location.href="/student"
    });

     
    $(document).on('click', '#build_new', function(){
       console.log("build new")
       window.location.href="/upload"
    });


    
    $(document).on('click', '#confirm_teacher', function(){
       console.log("to teacher")
       window.location.href="/teacher"
    });



    $(document).on('click', '#confirm_login_teacher', function(){
        var teacher_passwd=document.getElementById("teacher_passwd").value;
        var data_back={"teacher_passwd":teacher_passwd}       
        $.ajax({
	    type: 'POST',
	    url: "/teacher",
            data:data_back,
	    success: function (data) {
                    console.log(data);
		    if (data=="suc"){
		      window.location.href="/main_teacher";
		    }
                    else{
		      alert("密码错误，请重新登录");
		      window.location.href="/index";
		    }}
        });
    });


    $(document).on('click', '#get_history', function(){
                $.ajax({
	    type: 'POST',
	    url: "/get_history",
            data:{"info":"get_history"},
	    success: function (data) {
                    console.log(data);
		    if (data=="fail"){
		      alert("您还不能获取考试结果，可能还没有考试记录或者还没有上传试卷")
                      window.location.href="/"
		    }
                    else{
                      console.log("/"+data)
		      window.location.href=data;
		    }}
        });
 

       window.location.href="/get_history"
    });





    $(document).on('click', '#logout-btn', function(){
       window.location.href="/logout"
    });

    $(document).on('click', '#upload', function(){
		var formData = new FormData();//这里需要实例化一个FormData来进行文件上传
                the_file=document.getElementById("file_name").files[0];
                
		formData.append("file",the_file);
		$.ajax({
			type : "post",
			url : "upload",
			data : formData,
			processData : false,
			contentType : false,
			success : function(data){
				if (data=="fail") {
			              alert("文件提交失败!请按照标准格式提交文件！请使用记事本编辑，使用utf-8编码");
				}else{
				      confirm("文件上传成功!返回控制台！");
                                      window.location.href="/main_teacher";
			}}
		      });


               });

    

    
     $(document).on('click', '#submit_student', function(){
                        var ans = new FormData()
                        for (i=1;i<21;i++){
                        idd=i.toString();
                        var obj=document.getElementsByName(idd);
                        tmp=[]
                        for (k in obj){
                               if (obj[k].checked){
                                     tmp.push(obj[k].attributes.id.value)
                                 }}
                            console.log(tmp.toString());
                            tmps=tmp.toString()
                        ans.append(idd,tmps)
                          } 

                console.log(ans);

		$.ajax({
			type : "post",
			url : "submit_student",
			data : ans,
			processData : false,
			contentType : false,
			success : function(data){
				if (data=="fail") {
			              alert("提交失败，请联系后台！");
				}else{
				      confirm("答题成功！谢谢");
                                      window.location.href="/";
			}}
		      });


               })

    

    




    $(document).on('click', '#confirm_login_student', function(){
	var student_name=document.getElementById("student_name").value;
        var student_passwd=document.getElementById("student_passwd").value;
        var data_back={"student_name":student_name,
                       "student_passwd":student_passwd,
                      "x":x,
                      "y":y,
                      "city":city,
                      "pro":pro}       
        $.ajax({
	    type: 'POST',
	    url: "/student",
            data:data_back,
	    success: function (data) {
                    console.log(data);
		    if (data=="suc"){
		      window.location.href="/main_student";
		    }
                    else{
		    alert("账号密码错误，请重新登录");
		      window.location.href="/";
		    }}
        });
    });






});
