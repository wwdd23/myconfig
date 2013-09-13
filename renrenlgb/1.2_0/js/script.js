(function(){
	if($('.user-name').length==0)return;
	var url=window.location.href;
	var myid=$('#profileMenuActive a').attr('href').replace(/[^0-9]/ig,'');
	var requestToken=$('input[name=requestToken]').val();
	var _rtk=$('input[name="_rtk"]').val();
	var loading='加载中...';
	var finished='完成.';
	$('.site-menu-nav-box').prepend(
		'<div class="fs_title"><a>人人网分手器</a></div>\
		<div class="fs_panel '+(Number(localStorage.fs_panel)=='0'?'hide':'')+'">\
			<input type="text" id="fs_id" placeholder="对方的ID" value="" />\
			<div class="fs_item">\
				<label><input type="checkbox" id="fs_at_status" checked />@Ta的状态</label>\
				<label><input type="checkbox" id="fs_at_photo" checked />@Ta的照片</label>\
				<label><input type="checkbox" id="fs_at_share" checked />@Ta的分享</label>\
				<label><input type="checkbox" id="fs_status" checked />状态回复</label>\
				<label><input type="checkbox" id="fs_blog" checked />日志回复</label>\
				<label><input type="checkbox" id="fs_photo" checked />照片回复</label>\
				<label><input type="checkbox" id="fs_share" checked />分享回复</label>\
				<label><input type="checkbox" id="fs_msg" checked />站内信</label>\
				<label><input type="checkbox" id="fs_lovers" checked />情侣空间</label>\
				<label><input type="checkbox" id="fs_care" checked />特别关注</label>\
				<label><input type="checkbox" id="fs_relation" checked />好友关系</label>\
				<label><input type="checkbox" id="fs_black" checked />拉黑</label>\
				<label><input type="checkbox" id="fs_curse" checked />去留言板骂</label>\
			</div>\
			<div class="fs_option">\
				<a id="fs_all">全选</a>\
				<a id="fs_oppo">反选</a>\
				<button class="fs_btn">开始分手</button>\
			</div>\
		</div>'
	);
	$('.fs_title a').live('click',function(){
		localStorage.fs_panel!='0'&&localStorage.fs_panel!='1'?localStorage.fs_panel='1':null;
		localStorage.fs_panel=='0'?$('.fs_panel').removeClass('hide').show():$('.fs_panel').hide();
		localStorage.fs_panel=(1-Number(localStorage.fs_panel)).toString();
	});
	$('#fs_all').live('click',function(){
		$('.fs_item input').attr('checked','checked');
	});
	$('#fs_oppo').live('click',function(){
		$('.fs_item input').each(function(){
			$(this).attr('checked')?$(this).removeAttr('checked'):$(this).attr('checked','checked');
		});
	});
	$('.fs_btn').live('click',function(){
		var id=$('#fs_id').val();
		$('.fs_item input:checked').each(function(){
			var self=$(this);
			var type=self.attr('id');
			$('.'+type).remove();
			self.parents('label').after('<span class="loading '+type+'">'+loading+'</span>');
			eval(type+'('+id+')');
		});
	});
	function fs_at_status(id){
		var page=0;
		var doing=function(page){
			$.getJSON('http://status.renren.com/GetSomeomeDoingList.do?userId='+myid+'&curpage='+page,function(e){
				if(e.doingArray.length==0){
					$('.fs_at_status').html(finished);
					return;
				}
				page++;
				doing(page);
				for(i=0;i<e.doingArray.length;i++)
					if(e.doingArray[i].content.indexOf('namecard=\''+id+'\'')!=-1)
						$.post('http://status.renren.com/doing/deleteDoing.do','id='+e.doingArray[i].id+'&requestToken='+requestToken+'&_rtk='+_rtk);
			});
		}
		doing(page);
	}
	function fs_at_photo(id){
		$.post('http://photo.renren.com/ajaxcreatealbum.do','title=人人网分手器回收站&control=-1&password=&passwordProtected=false',function(e){
			var bin=e.albumid;
			$.get('http://photo.renren.com/photo/'+myid+'?__view=async-html-reload',function(e){
				var album_length=$('.album-cover',$(e)).length;
				album_length==0?$('.fs_at_photo').html(finished):null;
				$('.album-cover',$(e)).each(function(album_page){
					$.get($(this).attr('href'),function(f){
						var photo_length=$('input[value*="('+id+')"]',$(f)).length;
						photo_length==0?$('.fs_at_photo').html(finished):null;
						$('input[value*="('+id+')"]',$(f)).parents('li[data-info]').find('.picture').each(function(photo_page){
							$.post($(this).attr('href').split('?p')[0]+'/transfer','toId='+bin+'&sendFeed=1&requestToken='+requestToken+'&_rtk='+_rtk,function(){
								if(album_page+1==album_length&&photo_page+1==photo_length)$('.fs_at_photo').html(finished);
							});
						});
					});
				});
			});
		},'json');
	}
	function fs_at_share(id){
		var page=0;
		var doing=function(page){
			$.get('http://share.renren.com/share/'+myid+'?curpage='+page+'&type=0&__view=async-html',function(e){
				if($('.share-itembox',$(e)).length==0){
					$('.fs_at_share').html(finished);
					return;
				}
				page++;
				doing(page);
				for(i=0;i<$('.share-body',$(e)).length;i++)
					if($('.share-body',$(e)).eq(i).html().indexOf('namecard="'+id+'"')!=-1)
						$.post('http://share.renren.com/share/EditShare.do','action=del&sid='+$('.share-body',$(e)).eq(i).attr('id').split('share_box_')[1]+'&type='+myid+'&requestToken='+requestToken+'&_rtk='+_rtk);
			});
		}
		doing(page);
	}
	function fs_status(id){
		var page=0;
		var doing=function(page){
			$.getJSON('http://status.renren.com/GetSomeomeDoingList.do?userId='+myid+'&curpage='+page,function(e){
				if(e.doingArray.length==0){
					$('.fs_status').html(finished);
					return;
				}
				page++;
				doing(page);
				for(i=0;i<e.doingArray.length;i++){
					var doing_id=e.doingArray[i].id;
					$.post('http://status.renren.com/feedcommentretrieve.do','doingId='+doing_id+'&source='+doing_id+'&owner='+myid+'&t=3&requestToken='+requestToken+'&_rtk='+_rtk,function(f){
						for(j=0;j<f.replyList.length;j++){
							if(f.replyList[j].ubid==id){
								$.post('http://status.renren.com/feedcommentdelete.do','replyId='+f.replyList[j].id+'&source='+doing_id+'&doingId='+doing_id+'&owner='+myid+'&t=3&createId='+id+'&requestToken='+requestToken+'&_rtk='+_rtk);
							}
						}
					},'json');
				}
			});
		}
		doing(page);
	}
	function fs_blog(id){
		var page=0;
		var doing=function(page){
			$.get('http://blog.renren.com/blog/0?curpage='+page+'&__view=async-html',function(e){
				if($('.list-blog',$(e)).length==0){
					$('.fs_blog').html(finished);
					return;
				}
				page++;
				doing(page);
				$('.list-blog strong a',$(e)).each(function(){
					$.get($(this).attr('href'),function(f){
						f=JSON.parse(f.split('comments:')[1].split('});')[0]);
						for(i=0;i<f.comments.length;i++)
							if(f.comments[i].author==id)
								$.post('http://blog.renren.com/DelComment.do','id='+f.comments[i].id+'&owner='+myid+'&requestToken='+requestToken+'&_rtk='+_rtk);
					});
				});
			});
		}
		doing(page);
	}
	function fs_photo(id){
		$.get('http://photo.renren.com/photo/'+myid+'?__view=async-html-reload',function(e){
			var album_length=$('.album-cover',$(e)).length;
			album_length==0?$('.fs_photo').html(finished):null;
			$('.album-cover',$(e)).each(function(album_page){
				$.get($(this).attr('href'),function(f){
					var photo_length=$('.picture',$(f)).length;
					photo_length==0?$('.fs_photo').html(finished):null;
					$('.picture',$(f)).each(function(photo_page){
						var photo_href=$(this).attr('href').split('?p')[0];
						$.post(photo_href+'/ajax','psource=0&requestToken='+requestToken+'&_rtk='+_rtk,function(g){
							if(album_page+1==album_length&&photo_page+1==photo_length){
								$('.fs_photo').html(finished);
							}
							for(i=0;i<g.comments.length;i++)
								if(g.comments[i].author==id)
									$.post(photo_href+'/comment/'+g.comments[i].id+'/delete','requestToken='+requestToken+'&_rtk='+_rtk);
						},'json');
					});
				});
			});
		});
	}
	function fs_share(id){
		var page=0;
		var doing=function(page){
			$.get('http://share.renren.com/share/'+myid+'?curpage='+page+'&type=0&__view=async-html',function(e){
				if($('.share-itembox',$(e)).length==0){
					$('.fs_share').html(finished);
					return;
				}
				page++;
				doing(page);
				for(i=0;i<$('.share-body',$(e)).length;i++){
					var share_id=$('.share-body',$(e)).eq(i).attr('id').split('share_box_')[1];
					$.post('http://share.renren.com/share/showcomment.do','post={"share_id":'+share_id+',"share_owner":'+myid+'}&requestToken='+requestToken+'&_rtk='+_rtk,function(f){
						$('dd[id]',$(f)).each(function(){
							if($(this).find('.info>a').attr('namecard')==id)
								$.post('http://share.renren.com/share/deletecomment.do','post={"share_id":'+share_id+',"share_owner":'+myid+',"comment_id":'+$(this).attr('id').split('comment_')[1]+'}&requestToken='+requestToken+'&_rtk='+_rtk);
						});
					});
				}
			});
		}
		doing(page);
	}
	function fs_msg(id){
		var page=0;
		var doing=function(page){
			$.get('http://msg.renren.com/message/inbox.do?curpage='+page+'&f=0',function(e){
				if(e.indexOf('当前没有任何站内信')!=-1){
					$('.fs_msg').html(finished);
					return;
				}
				page++;
				doing(page);
				$('.message_rows tr',$(e)).each(function(){
					if($(this).find('.name_and_date a').eq(0).attr('href').indexOf(id)!=-1)
						$.get('http://msg.renren.com/message/ajax.do?post={"action":"delete","ids":['+$(this).attr('id').split('thread_')[1]+'],"folder":0,"unread_count":0,"slice":20}');
				});
			});
		}
		doing(page);
	}
	function fs_lovers(id){
		$.get('http://lover.renren.com/home',function(e){
			if($('.mylove-desc',$(e)).length==0){
				$('.fs_lovers').html(finished);
				return;
			}
			var pid=$('.mylove-desc a',$(e)).attr('href').split('.com')[1].split('?ref')[0];
				$.post('http://lover.renren.com/settings/setClosed','pid='+pid+'&lament=&isOpen=false&requestToken='+requestToken+'&_rtk='+_rtk,function(){
					$('.fs_lovers').html(finished);
				});
		});
	}
	function fs_care(id){
		$.post('http://www.renren.com/relationFeedOper.do?action=delHigh','id='+id+'&requestToken='+requestToken+'&_rtk='+_rtk,function(){
			$('.fs_care').html(finished);
		});
	}
	function fs_relation(id){
		$.post('http://friend.renren.com/DelFriend.do','id='+id+'&code=null&codeFlag=0&requestToken='+requestToken+'&_rtk='+_rtk,function(){
			$('.fs_relation').html(finished);
		});
	}
	function fs_black(id){
		$.post('http://friend.renren.com/j_f_add_block','id='+id+'&_rtk='+_rtk,function(){
			$('.fs_black').html(finished);
		});
	}
	function fs_curse(id){
		$.get('http://www.renren.com/'+id,function(e){
			var ak=$('input[name="ak"]',$(e)).val();
			$.post('http://gossip.renren.com/gossip.do','body=呵呵&curpage=&from=main&id='+id+'&cc='+id+'&ak='+ak+'&cccc=&tsc=&ref=http://www.renren.com/profile/'+id+'&profilever=2008&headUrl=&largeUrl=&only_to_me=0&color=&requestToken='+requestToken+'&_rtk='+_rtk,function(){
				$('.fs_curse').html(finished);
			});
		});
	}
})();
