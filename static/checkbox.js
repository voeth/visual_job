var maxChoices = 2;
var flag = 0;

function onCheckBox(checkbox)
{
	var items = document.getElementsByName("item");
	//var maxChoices = 2;
	//var flag = 0;

	if(checkbox.checked)
	{
		flag ++;
	}
	else
	{
		flag --;
	}

	if(flag < maxChoices)
	{
		for(var i=0; i<items.length; i++)
		{
			if(!items[i].checked)
			{
				items[i].disabled = false;
			}
		}
	}
	else
	{
		for(var i=0; i<items.length; i++)
		{
			if(!items[i].checked)
			{
				items[i].disabled = true;
			}
		}
	}


}

function onSubmitVote()
{
	var items = document.getElementsByName("item");
	var choices = 0;
	//var maxChoices = 3;

	for(var j=0; j<items.length; j++)
	{
		if(items[j].checked)
		{
			choices ++;
		}
	}
	if(choices == 0)
	{
		alert("请选择选项再提交");
	}
	else if(choices > maxChoices)
	{
		alert("选择选项不能超过 "+ maxChoices + "个");
	}
	else
	{
		alert("提交成功");
	}
}