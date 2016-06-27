$('#searchButton').click(function(){
	var name=$('#searchBox').val();
	getData(name);
});

var getData=function(name){
	$.ajax({
	url:'/getData/'+name,
	type:'GET',
	success:function(result)
	{
		showTweets(JSON.parse(result))	
	}
	});
}

var showTweets=function(jsonObject){
	//Resetting the table
	$('#tweetTable').empty();
	for(var  i=0;i<jsonObject.length;i++)
	{
		//Converting date to appropriate format
		var date = new Date(jsonObject[i].created_at); //creating a date object  
		var created_at = date.toUTCString();
		var tableString='<tr><td>'
		+jsonObject[i]['user.screen_name']+'</td>'
		+'<td>'+created_at+'</td><td>'
		+jsonObject[i]['text']+'</td><td>'
		+jsonObject[i]['hashtags'].join(',')+'</td><td>'
		+jsonObject[i]['retweet_count']+'</td><td>'
		+jsonObject[i]['sentiment']
		+'</td></tr>';
		//Appending each row to table iteratively
		$('#tweetTable').append(tableString);
	}
}

/*Sort by sentiments*/
$('#sentimentHeader').click(function(){
    globalTweets.sort(function(x, y){
        return parseFloat(y.sentiment)-parseFloat(x.sentiment);   
    })
    showTweets(globalTweets);
})

/*Sort retweets*/
$('#retweetHeader').click(function(){
    globalTweets.sort(function(x, y){
        return parseFloat(y.retweet_count)-parseFloat(x.retweet_count);   
    })
    showTweets(globalTweets);
})
