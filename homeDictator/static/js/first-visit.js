$(document).ready(function(){

	function read_cookie(key){
	    var result;
	    return (result = new RegExp('(?:^|; )' + encodeURIComponent(key) + '=([^;]*)').exec(document.cookie)) ? (result[1]) : null;
	};

	console.log(read_cookie('old_user'));
	old_user=read_cookie('old_user');

	if(old_user == "true"){
		var expiration_date = new Date();
		var cookie_string = '';
		expiration_date.setFullYear(expiration_date.getFullYear() + 1);
		// Build the set-cookie string:
		cookie_string = "old_user=true; path=/; expires=" + expiration_date.toUTCString();
		// Create or update the cookie:
		document.cookie = cookie_string;
	};
	if (!old_user){
		$('#tap-add').tapTarget('open');
		var expiration_date = new Date();
		var cookie_string = '';
		expiration_date.setFullYear(expiration_date.getFullYear() + 1);
		// Build the set-cookie string:
		cookie_string = "old_user=true; path=/; expires=" + expiration_date.toUTCString();
		// Create or update the cookie:
		document.cookie = cookie_string;
	};
});
