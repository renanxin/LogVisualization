function sel() {
	var observe=document.getElementById("windowsType");
	if (observe.value=="0") {
		var pTime=document.getElementById("pTime");//显示
			pTime.style.display="block";
		var pNumber=document.getElementById("pNumber");//隐藏
			pNumber.style.display="none";
	}
	else if (observe.value=="1") {
		var pTime=document.getElementById("pTime");//隐藏
			pTime.style.display="none";
		var pNumber=document.getElementById("pNumber");//显示
			pNumber.style.display="block"; 
	}

}


var observe=document.getElementById("windowsType");
if (observe.value=="0") {
	var pTime=document.getElementById("pTime");//显示
		pTime.style.display="block";
	var pNumber=document.getElementById("pNumber");//隐藏
			pNumber.style.display="none";
}
