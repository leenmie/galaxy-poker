function CafeCaptcha(captcha_area_id) {
	var special_chars = ['&#x2660;', '&#x2663;', '&#x2666;', '&#x2665;'];
	//var captcha_area_id_jq = '#' + captcha_area_id
	var get_card_string = function(value) {
		var number = (~~(value / 4)) + 1;
		var kind = value % 4;
		var str_number;
		if ((number >=2) && (number <=10)) {
			str_number = number.toString();
		}
		else if (number == 1) {
			str_number = 'A';
		}
		else if (number == 11) {
			str_number = 'J';
		}
		else if (number == 12) {
			str_number = 'Q';
		}
		else if (number == 13) {
			str_number = 'K';
		}
		str_number = str_number + special_chars[kind];
		return str_number;				
	};		
	var select_image_card_string = function() {
		var kind_color = ["blue","green","orange","red"];
		var i;
		var option_values = '';
		for (i=0; i<52; i++) {
			cardstring = get_card_string(i);
			var kind = i % 4;
			option_values += '<option value="'+
							i.toString()+
							'" style="color:'+
							kind_color[kind]+
							';">'+
							cardstring+
							'</option>';
		}
		var selecthtml = '';
		for (i=0; i<3; i++) {
			selecthtml += '<select style="font-size:40px;" id="captcha_answer_id'+i.toString() + '" '+
							'onchange="reload_captcha_response_value();"'+
							'>';
			selecthtml += option_values;
			selecthtml += '</select>';
		}
		return selecthtml;
	};
	
	reload_captcha_response_value = function() {
		var response_value = $("#captcha_answer_id0").val()+ '|' +
							$("#captcha_answer_id1").val()+ '|' +
							$("#captcha_answer_id2").val();
		$("#recaptcha_response_field").val(response_value);
		//console.log(response_value);
	};
	
	var loadDefaultCaptcha = function(turingtestid) {
		var addhtml = "<img src=\"/service/captcha?turingtestid=" +
						turingtestid +
						'"> </img>';
		addhtml += "<br/>" + select_image_card_string();
		addhtml += '<input type="hidden" name="recaptcha_challenge_field"'+
				'id="recaptcha_challenge_field" value="'+
				turingtestid+
				'"></input>';
		addhtml += '<input type="hidden" name="recaptcha_response_field"'+
				'id="recaptcha_response_field" value="0|0|0">'+
				'</input>';
		//console.log(addhtml);
		$('#'+captcha_area_id).append(addhtml);
	};
	var loadRecatpcha = function() {
		 Recaptcha.create("6LdSatUSAAAAAKEZMQcmxpItYlNUcciO4SvSeLoH",
		    				captcha_area_id,
						    {
						      theme: "red",
						      callback: Recaptcha.focus_response_field
						    }
						  );
	};
	this.loadCaptcha = function() {
		$('#'+captcha_area_id).empty();
		$.getJSON("/service/captcha", function(jsondata) {
			var captcha_result = jsondata.result;
			//console.log(captcha_result);
			if (captcha_result == 0) {
				var captcha_turingtestid = jsondata.turingtestid;
				loadDefaultCaptcha(captcha_turingtestid);
			}
			else {
				loadRecatpcha();
			}
		});		
	};		
}