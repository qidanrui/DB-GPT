(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[929],{83738:function(e,l,t){Promise.resolve().then(t.bind(t,65641))},65641:function(e,l,t){"use strict";t.r(l),t.d(l,{default:function(){return X}});var n=t(9268),i=t(86006),a=t(91440),s=t(90022),r=t(69962),o=t(97287),d=t(73141),c=t(45642),u=t(8997),h=t(22046),x=t(83192),v=t(90545),p=t(89081),f=t(78915),m=t(71990),j=e=>{let l=(0,i.useReducer)((e,l)=>({...e,...l}),{...e});return l},b=t(57931),g=t(52040),y=e=>{let{queryAgentURL:l,channel:t,queryBody:n,initHistory:a,runHistoryList:s}=e,[r,o]=j({history:a||[]}),{refreshDialogList:d}=(0,b.Cg)(),c=new AbortController;(0,i.useEffect)(()=>{a&&o({history:a})},[a]);let u=async(e,i)=>{if(!e)return;let a=[...r.history,{role:"human",context:e}],s=a.length;o({history:a});try{await (0,m.L)("".concat(g.env.API_BASE_URL?g.env.API_BASE_URL:"").concat("/api"+l),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({...i,...n,user_input:e,channel:t}),signal:c.signal,async onopen(e){if(a.length<=1){var l;d();let e=new URLSearchParams(window.location.search);e.delete("initMessage"),null===(l=window.history)||void 0===l||l.replaceState(null,null,"?".concat(e.toString()))}(!e.ok||e.headers.get("content-type")!==m.a)&&e.status>=400&&e.status<500&&429!==e.status&&e.status},onclose(){console.log("onclose")},onerror(e){throw console.log("onerror"),Error(e)},onmessage:e=>{var l,t,n;if(e.data=null===(l=e.data)||void 0===l?void 0:l.replaceAll("\\n","\n"),"[DONE]"===e.data);else if(null===(t=e.data)||void 0===t?void 0:t.startsWith("[ERROR]"))o({history:[...a,{role:"view",context:null===(n=e.data)||void 0===n?void 0:n.replace("[ERROR]","")}]});else{let l=[...a];e.data&&((null==l?void 0:l[s])?l[s].context="".concat(e.data):l.push({role:"view",context:e.data}),o({history:l}))}}})}catch(e){console.log(e),o({history:[...a,{role:"view",context:"请求出错"}]})}};return{handleChatSubmit:u,history:r.history}},_=t(67830),w=t(54842),Z=t(80937),N=t(311),P=t(94244),C=t(12025),S=t(46571),k=t(53113),E=t(35086),D=t(53047),R=t(81528),O=t(30530),L=t(64747),B=t(77614),I=t(19700),T=t(92391),A=t(55749),z=t(70781),F=t(75403),V=t(99398),q=t(49064),J=t(56008),M=t(84835),U=t.n(M),W=t(21628),H=t(15241),G=t(28179);let K=T.z.object({query:T.z.string().min(1)});var Y=e=>{var l;let{messages:a,onSubmit:r,readOnly:o,paramsList:d,runParamsList:c,isChartChat:u=!1,dbList:h,runDbList:p,supportTypes:m,clearIntialMessage:j,setChartsData:b}=e,g=(0,J.useSearchParams)(),y=g.get("initMessage"),T=g.get("spaceNameOriginal"),M=g.get("scene"),Y=(0,i.useRef)(null),[Q,X]=(0,i.useState)(!1),[$,ee]=(0,i.useState)(),[el,et]=(0,i.useState)(!1),[en,ei]=(0,i.useState)(),[ea,es]=(0,i.useState)(a),[er,eo]=(0,i.useState)(""),[ed,ec]=(0,i.useState)(!1),[eu,eh]=(0,i.useState)(h),ex=(e,l,t)=>{let n=U().cloneDeep(eu);n&&(void 0===(null==eu?void 0:eu[e])&&(n[e]={}),n[e][l]=t,eh(n))},ev=(0,I.cI)({resolver:(0,_.F)(K),defaultValues:{}}),ep=async e=>{let{query:l}=e;try{X(!0),ev.reset(),await r(l,{select_param:null==d?void 0:d[$]})}catch(e){}finally{X(!1)}},ef=async()=>{try{var e;let l=new URLSearchParams(window.location.search),t=l.get("initMessage");l.delete("initMessage"),null===(e=window.history)||void 0===e||e.replaceState(null,null,"?".concat(l.toString())),await ep({query:t})}catch(e){console.log(e)}finally{null==j||j()}},em={overrides:{code:e=>{let{children:l}=e;return(0,n.jsx)(V.Z,{language:"javascript",style:q.Z,children:l})}},wrapper:i.Fragment},ej=e=>{let l=e;try{l=JSON.parse(e)}catch(e){console.log(e)}return l},eb=i.useMemo(()=>{if("function"==typeof(null==window?void 0:window.fetch)){let e=t(62631);return t(25204),t(82372),e.default}},[]);return i.useEffect(()=>{Y.current&&Y.current.scrollTo(0,Y.current.scrollHeight)},[null==a?void 0:a.length]),i.useEffect(()=>{y&&a.length<=0&&ef()},[y,a.length]),i.useEffect(()=>{var e,l;d&&(null===(e=Object.keys(d||{}))||void 0===e?void 0:e.length)>0&&ee(T||(null===(l=Object.keys(d||{}))||void 0===l?void 0:l[0]))},[d]),i.useEffect(()=>{if(u){let e=U().cloneDeep(a);e.forEach(e=>{(null==e?void 0:e.role)==="view"&&"string"==typeof(null==e?void 0:e.context)&&(e.context=ej(null==e?void 0:e.context))}),es(e.filter(e=>["view","human"].includes(e.role)))}else es(a.filter(e=>["view","human"].includes(e.role)))},[u,a]),(0,i.useEffect)(()=>{let e=U().cloneDeep(h);null==e||e.forEach(e=>{let l=null==m?void 0:m.find(l=>l.db_type===e.db_type);e.isfileDb=null==l?void 0:l.is_file_db}),eh(e)},[h,m]),(0,n.jsxs)("div",{className:"w-full h-full",children:[(0,n.jsxs)(Z.Z,{className:"w-full h-full bg-[#fefefe] dark:bg-[#212121]",sx:{table:{borderCollapse:"collapse",border:"1px solid #ccc",width:"100%"},"th, td":{border:"1px solid #ccc",padding:"10px",textAlign:"center"}},children:[(0,n.jsxs)(Z.Z,{ref:Y,direction:"column",sx:{overflowY:"auto",maxHeight:"100%",flex:1},children:[null==ea?void 0:ea.map((e,l)=>{var t,i;return(0,n.jsx)(Z.Z,{children:(0,n.jsx)(s.Z,{size:"sm",variant:"outlined",color:"view"===e.role?"primary":"neutral",sx:l=>({background:"view"===e.role?"var(--joy-palette-primary-softBg, var(--joy-palette-primary-100, #DDF1FF))":"unset",border:"unset",borderRadius:"unset",padding:"24px 0 26px 0",lineHeight:"24px"}),children:(0,n.jsxs)(v.Z,{sx:{width:"76%",margin:"0 auto"},className:"flex flex-row",children:[(0,n.jsx)("div",{className:"mr-3 inline",children:"view"===e.role?(0,n.jsx)(z.Z,{}):(0,n.jsx)(A.Z,{})}),(0,n.jsx)("div",{className:"inline align-middle mt-0.5 max-w-full flex-1 overflow-auto",children:u&&"view"===e.role&&"object"==typeof(null==e?void 0:e.context)?(0,n.jsxs)(n.Fragment,{children:["[".concat(e.context.template_name,"]: "),(0,n.jsx)(N.Z,{sx:{color:"#1677ff"},component:"button",onClick:()=>{et(!0),ei(l),eo(JSON.stringify(null==e?void 0:e.context,null,2))},children:e.context.template_introduce||"暂无介绍"})]}):(0,n.jsx)(F.Z,{options:em,children:null===(t=e.context)||void 0===t?void 0:null===(i=t.replaceAll)||void 0===i?void 0:i.call(t,"\\n","\n")})})]})})},l)}),Q&&(0,n.jsx)(P.Z,{variant:"soft",color:"neutral",size:"sm",sx:{mx:"auto",my:2}})]}),!o&&(0,n.jsx)(v.Z,{className:"bg-[#fefefe] dark:bg-[#212121] before:bg-[#fefefe] before:dark:bg-[#212121]",sx:{position:"relative","&::before":{content:'" "',position:"absolute",top:"-18px",left:"0",right:"0",width:"100%",margin:"0 auto",height:"20px",filter:"blur(10px)",zIndex:2}},children:(0,n.jsxs)("form",{style:{maxWidth:"100%",width:"76%",position:"relative",display:"flex",marginTop:"auto",overflow:"visible",background:"none",justifyContent:"center",marginLeft:"auto",marginRight:"auto",flexDirection:"column",gap:"12px",paddingBottom:"58px",paddingTop:"20px"},onSubmit:e=>{e.stopPropagation(),ev.handleSubmit(ep)(e)},children:[(0,n.jsxs)("div",{style:{display:"flex",gap:"8px"},children:[Object.keys(d||{}).length>0&&(0,n.jsx)("div",{className:"flex items-center gap-3",children:(0,n.jsx)(C.Z,{value:$,onChange:(e,l)=>{ee(l)},sx:{maxWidth:"100%"},children:null===(l=Object.keys(d||{}))||void 0===l?void 0:l.map(e=>(0,n.jsx)(S.Z,{value:e,children:e},e))})}),["chat_with_db_execute","chat_with_db_qa"].includes(M)&&(0,n.jsx)(k.Z,{"aria-label":"Like",variant:"plain",color:"neutral",sx:{padding:0,"&: hover":{backgroundColor:"unset"}},onClick:()=>{ec(!0)},children:(0,n.jsxs)("div",{style:{display:"flex",alignItems:"center"},children:[(0,n.jsx)(G.Z,{style:{marginBottom:"0.125rem",fontSize:"28px"}}),(0,n.jsx)("span",{style:{display:"block",lineHeight:"25px",fontSize:12,marginLeft:6},children:"DB Connect Setting"})]})})]}),(0,n.jsx)(E.ZP,{className:"w-full h-12",variant:"outlined",endDecorator:(0,n.jsx)(D.ZP,{type:"submit",disabled:Q,children:(0,n.jsx)(w.Z,{})}),...ev.register("query")})]})})]}),(0,n.jsx)(R.Z,{open:el,onClose:()=>{et(!1)},children:(0,n.jsxs)(O.Z,{"aria-labelledby":"variant-modal-title","aria-describedby":"variant-modal-description",children:[(0,n.jsx)(L.Z,{}),(0,n.jsxs)(v.Z,{sx:{marginTop:"32px"},children:[!!eb&&(0,n.jsx)(eb,{mode:"json",value:er,height:"600px",width:"820px",onChange:eo,placeholder:"默认json数据",debounceChangePeriod:100,showPrintMargin:!0,showGutter:!0,highlightActiveLine:!0,setOptions:{useWorker:!0,showLineNumbers:!0,highlightSelectedWord:!0,tabSize:2}}),(0,n.jsx)(k.Z,{variant:"outlined",className:"w-full",sx:{marginTop:"12px"},onClick:()=>{if(en)try{let e=U().cloneDeep(ea),l=JSON.parse(er);e[en].context=l,es(e),null==b||b(null==l?void 0:l.charts),et(!1),eo("")}catch(e){W.ZP.error("JSON 格式化出错")}},children:"Submit"})]})]})}),(0,n.jsx)(R.Z,{open:ed,onClose:()=>{ec(!1),null==c||c()},children:(0,n.jsxs)(O.Z,{children:[(0,n.jsx)(L.Z,{}),(0,n.jsxs)(x.Z,{children:[(0,n.jsx)("caption",{children:(0,n.jsx)("h3",{style:{fontWeight:"bold"},children:"数据库列表"})}),(0,n.jsx)("thead",{children:(0,n.jsxs)("tr",{children:[(0,n.jsx)("th",{style:{width:"140px"},children:"数据库类型"}),(0,n.jsx)("th",{style:{width:"130px"},children:"数据库名"}),(0,n.jsx)("th",{style:{width:"150px"},children:"链接地址/域名"}),(0,n.jsx)("th",{style:{width:"100px"},children:"端口"}),(0,n.jsx)("th",{style:{width:"140px"},children:"用户名"}),(0,n.jsx)("th",{style:{width:"140px"},children:"密码"}),(0,n.jsx)("th",{style:{width:"140px"},children:"备注"}),(0,n.jsx)("th",{style:{width:"140px"},children:"操作"})]})}),(0,n.jsxs)("tbody",{children:[null==eu?void 0:eu.map((e,l)=>(0,n.jsxs)("tr",{children:[(0,n.jsx)("td",{children:(null==e?void 0:e.isEdit)?(0,n.jsx)(C.Z,{defaultValue:null==e?void 0:e.db_type,onChange:(e,t)=>{let n=null==m?void 0:m.find(e=>e.db_type===t),i=U().cloneDeep(eu);i[l].db_type=t,i[l].isfileDb=null==n?void 0:n.is_file_db,n?(i[l].db_host="",i[l].db_port=""):i[l].db_path="",eh(i)},children:null==m?void 0:m.map(e=>(0,n.jsx)(S.Z,{value:e.db_type,children:null==e?void 0:e.db_type},e.db_type))}):(0,n.jsx)(H.Z,{title:null==e?void 0:e.db_type,children:null==e?void 0:e.db_type})}),(0,n.jsx)("td",{children:(null==e?void 0:e.isNew)?(0,n.jsx)(E.ZP,{value:null==e?void 0:e.db_name,onChange:e=>{ex(l,"db_name",e.target.value)}}):(0,n.jsx)(H.Z,{title:null==e?void 0:e.db_name,children:null==e?void 0:e.db_name})}),(0,n.jsx)("td",{children:(null==e?void 0:e.isEdit)?(0,n.jsx)(E.ZP,{value:(null==e?void 0:e.isfileDb)?null==e?void 0:e.db_path:null==e?void 0:e.db_host,onChange:t=>{(null==e?void 0:e.isfileDb)?ex(l,"db_path",t.target.value):ex(l,"db_host",t.target.value)}}):(0,n.jsx)(H.Z,{title:(null==e?void 0:e.isfileDb)?null==e?void 0:e.db_path:null==e?void 0:e.db_host,children:(null==e?void 0:e.isfileDb)?null==e?void 0:e.db_path:null==e?void 0:e.db_host})}),(0,n.jsx)("td",{children:(null==e?void 0:e.isEdit)?(null==e?void 0:e.isfileDb)?"-":(0,n.jsx)(E.ZP,{value:null==e?void 0:e.db_port,onChange:e=>{ex(l,"db_port",e.target.value)}}):(0,n.jsx)(H.Z,{title:null==e?void 0:e.db_port,children:null==e?void 0:e.db_port})}),(0,n.jsx)("td",{children:(null==e?void 0:e.isEdit)?(0,n.jsx)(E.ZP,{defaultValue:e.db_user,onChange:e=>{ex(l,"db_user",e.target.value)}}):(0,n.jsx)(H.Z,{title:null==e?void 0:e.db_user,children:null==e?void 0:e.db_user})}),(0,n.jsx)("td",{children:(null==e?void 0:e.isEdit)?(0,n.jsx)(E.ZP,{defaultValue:e.db_pwd,type:"password",onChange:e=>{ex(l,"db_pwd",e.target.value)}}):(0,n.jsx)(n.Fragment,{children:"******"})}),(0,n.jsx)("td",{children:(null==e?void 0:e.isEdit)?(0,n.jsx)(E.ZP,{defaultValue:null==e?void 0:e.comment,onChange:e=>{ex(l,"comment",e.target.value)}}):(0,n.jsx)(H.Z,{title:null==e?void 0:e.comment,children:null==e?void 0:e.comment})}),(0,n.jsx)("td",{children:(0,n.jsxs)(v.Z,{sx:{gap:1,["& .".concat(B.Z.root)]:{padding:0,"&:hover":{background:"transparent"}}},children:[(null==e?void 0:e.isEdit)?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(k.Z,{size:"sm",variant:"plain",color:"neutral",sx:{marginRight:"8px"},onClick:async()=>{let l=U().cloneDeep(e),t={db_type:null==l?void 0:l.db_type,db_name:null==l?void 0:l.db_name,file_path:(null==l?void 0:l.isfileDb)?null==l?void 0:l.db_path:void 0,db_host:(null==l?void 0:l.isfileDb)?void 0:null==l?void 0:l.db_host,db_port:(null==l?void 0:l.isfileDb)?void 0:null==l?void 0:l.db_port,db_user:null==l?void 0:l.db_user,db_pwd:null==l?void 0:l.db_pwd,comment:null==l?void 0:l.comment};if(l.isNew){let e=null==h?void 0:h.map(e=>null==e?void 0:e.db_name);if(null==e?void 0:e.includes(null==l?void 0:l.db_name)){W.ZP.error("该数据库名称已存在");return}await (0,f.PR)("/api/v1/chat/db/add",t)}else await (0,f.PR)("/api/v1/chat/db/edit",t);await (null==p?void 0:p())},children:"保存"}),(0,n.jsx)(k.Z,{size:"sm",variant:"plain",color:"neutral",sx:{marginRight:"8px"},onClick:()=>{let t=U().cloneDeep(eu);(null==e?void 0:e.isNew)?t.splice(l,1):(t[l].isEdit=!1,t[l]=null==h?void 0:h[l]),eh(t)},children:"取消"})]}):(0,n.jsx)(k.Z,{size:"sm",variant:"plain",color:"neutral",sx:{marginRight:"8px"},onClick:()=>{let e=U().cloneDeep(eu);e[l].isEdit=!0,eh(e)},children:"编辑"}),(0,n.jsx)(k.Z,{size:"sm",variant:"soft",color:"danger",onClick:async()=>{(null==e?void 0:e.db_name)&&(await (0,f.PR)("/api/v1/chat/db/delete?db_name=".concat(null==e?void 0:e.db_name)),await (null==p?void 0:p()))},children:"删除"})]})})]},l)),(0,n.jsx)("tr",{children:(0,n.jsx)("td",{colSpan:8,children:(0,n.jsx)(k.Z,{variant:"outlined",sx:{width:"100%"},onClick:()=>{let e=U().cloneDeep(eu);null==e||e.push({isEdit:!0,isNew:!0,db_name:""}),eh(e)},children:"+ 新增一行"})})})]})]})]})})]})};let Q=()=>(0,n.jsxs)(s.Z,{className:"h-full w-full flex bg-transparent",children:[(0,n.jsx)(r.Z,{animation:"wave",variant:"text",level:"body2"}),(0,n.jsx)(r.Z,{animation:"wave",variant:"text",level:"body2"}),(0,n.jsx)(o.Z,{ratio:"21/9",className:"flex-1",sx:{["& .".concat(d.Z.content)]:{height:"100%"}},children:(0,n.jsx)(r.Z,{variant:"overlay",className:"h-full"})})]});var X=()=>{let[e,l]=(0,i.useState)();i.useRef(null);let[t,r]=i.useState(!1),o=(0,J.useSearchParams)(),{refreshDialogList:d}=(0,b.Cg)(),m=o.get("id"),j=o.get("scene"),{data:g,run:_}=(0,p.Z)(async()=>await (0,f.Tk)("/v1/chat/dialogue/messages/history",{con_uid:m}),{ready:!!m,refreshDeps:[m]}),{data:w,run:Z}=(0,p.Z)(async()=>await (0,f.Tk)("/v1/chat/db/list"),{ready:!!j&&!!["chat_with_db_execute","chat_with_db_qa"].includes(j)}),{data:N}=(0,p.Z)(async()=>await (0,f.Tk)("/v1/chat/db/support/type"),{ready:!!j&&!!["chat_with_db_execute","chat_with_db_qa"].includes(j)}),{data:P,run:C}=(0,p.Z)(async()=>await (0,f.Kw)("/v1/chat/mode/params/list?chat_mode=".concat(j)),{ready:!!j,refreshDeps:[m,j]}),{history:S,handleChatSubmit:k}=y({queryAgentURL:"/v1/chat/completions",queryBody:{conv_uid:m,chat_mode:j||"chat_normal"},initHistory:null==g?void 0:g.data,runHistoryList:_});(0,i.useEffect)(()=>{try{var e;let t=null==S?void 0:null===(e=S[S.length-1])||void 0===e?void 0:e.context,n=JSON.parse(t);l((null==n?void 0:n.template_name)==="report"?null==n?void 0:n.charts:void 0)}catch(e){l(void 0)}},[S]);let E=(0,i.useMemo)(()=>{if(e){let l=[],t=null==e?void 0:e.filter(e=>"IndicatorValue"===e.chart_type);t.length>0&&l.push({rowIndex:l.length,cols:t,type:"IndicatorValue"});let n=null==e?void 0:e.filter(e=>"IndicatorValue"!==e.chart_type),i=n.length,a=0;return[[0],[1],[2],[1,2],[1,3],[2,1,2],[2,1,3],[3,1,3],[3,2,3]][i].forEach(e=>{if(e>0){let t=n.slice(a,a+e);a+=e,l.push({rowIndex:l.length,cols:t})}}),l}},[e]);return(0,n.jsxs)(c.Z,{container:!0,spacing:2,className:"h-full",sx:{flexGrow:1},children:[e&&(0,n.jsx)(c.Z,{xs:8,className:"max-h-full",children:(0,n.jsx)("div",{className:"flex flex-col gap-3 h-full",children:null==E?void 0:E.map(e=>(0,n.jsx)("div",{className:"".concat((null==e?void 0:e.type)!=="IndicatorValue"?"flex flex-1 gap-3 overflow-hidden":""),children:e.cols.map(e=>{if("IndicatorValue"===e.chart_type)return(0,n.jsx)("div",{className:"flex flex-row gap-3",children:e.values.map(e=>(0,n.jsx)("div",{className:"flex-1",children:(0,n.jsx)(s.Z,{sx:{background:"transparent"},children:(0,n.jsxs)(u.Z,{className:"justify-around",children:[(0,n.jsx)(h.ZP,{gutterBottom:!0,component:"div",children:e.name}),(0,n.jsx)(h.ZP,{children:e.value})]})})},e.name))},e.chart_uid);if("LineChart"===e.chart_type)return(0,n.jsx)("div",{className:"flex-1 overflow-hidden",children:(0,n.jsx)(s.Z,{className:"h-full",sx:{background:"transparent"},children:(0,n.jsxs)(u.Z,{className:"h-full",children:[(0,n.jsx)(h.ZP,{gutterBottom:!0,component:"div",children:e.chart_name}),(0,n.jsx)(h.ZP,{gutterBottom:!0,level:"body3",children:e.chart_desc}),(0,n.jsx)("div",{className:"flex-1 h-full",children:(0,n.jsx)(a.Chart,{padding:[10,20,50,40],autoFit:!0,data:e.values,children:(0,n.jsx)(a.LineAdvance,{shape:"smooth",point:!0,area:!0,position:"name*value",color:"type"})})})]})})},e.chart_uid);if("BarChart"===e.chart_type)return(0,n.jsx)("div",{className:"flex-1",children:(0,n.jsx)(s.Z,{className:"h-full",sx:{background:"transparent"},children:(0,n.jsxs)(u.Z,{className:"h-full",children:[(0,n.jsx)(h.ZP,{gutterBottom:!0,component:"div",children:e.chart_name}),(0,n.jsx)(h.ZP,{gutterBottom:!0,level:"body3",children:e.chart_desc}),(0,n.jsx)("div",{className:"flex-1",children:(0,n.jsxs)(a.Chart,{autoFit:!0,data:e.values,children:[(0,n.jsx)(a.Interval,{position:"name*value",style:{lineWidth:3,stroke:(0,a.getTheme)().colors10[0]}}),(0,n.jsx)(a.Tooltip,{shared:!0})]})})]})})},e.chart_uid);if("Table"===e.chart_type){var l,t;let i=U().groupBy(e.values,"type");return(0,n.jsx)("div",{className:"flex-1",children:(0,n.jsx)(s.Z,{className:"h-full overflow-auto",sx:{background:"transparent"},children:(0,n.jsxs)(u.Z,{className:"h-full",children:[(0,n.jsx)(h.ZP,{gutterBottom:!0,component:"div",children:e.chart_name}),(0,n.jsx)(h.ZP,{gutterBottom:!0,level:"body3",children:e.chart_desc}),(0,n.jsx)("div",{className:"flex-1",children:(0,n.jsxs)(x.Z,{"aria-label":"basic table",stripe:"odd",hoverRow:!0,borderAxis:"bothBetween",children:[(0,n.jsx)("thead",{children:(0,n.jsx)("tr",{children:Object.keys(i).map(e=>(0,n.jsx)("th",{children:e},e))})}),(0,n.jsx)("tbody",{children:null===(l=Object.values(i))||void 0===l?void 0:null===(t=l[0])||void 0===t?void 0:t.map((e,l)=>{var t;return(0,n.jsx)("tr",{children:null===(t=Object.keys(i))||void 0===t?void 0:t.map(e=>{var t;return(0,n.jsx)("td",{children:(null==i?void 0:null===(t=i[e])||void 0===t?void 0:t[l].value)||""},e)})},l)})})]})})]})})},e.chart_uid)}})},e.rowIndex))})}),!e&&"chat_dashboard"===j&&(0,n.jsx)(c.Z,{xs:8,className:"max-h-full p-6",children:(0,n.jsx)("div",{className:"flex flex-col gap-3 h-full",children:(0,n.jsxs)(c.Z,{container:!0,spacing:2,sx:{flexGrow:1},children:[(0,n.jsx)(c.Z,{xs:8,children:(0,n.jsx)(v.Z,{className:"h-full w-full",sx:{display:"flex",gap:2},children:(0,n.jsx)(Q,{})})}),(0,n.jsx)(c.Z,{xs:4,children:(0,n.jsx)(Q,{})}),(0,n.jsx)(c.Z,{xs:4,children:(0,n.jsx)(Q,{})}),(0,n.jsx)(c.Z,{xs:8,children:(0,n.jsx)(Q,{})})]})})}),(0,n.jsx)(c.Z,{xs:"chat_dashboard"===j?4:12,className:"h-full max-h-full",children:(0,n.jsx)("div",{className:"h-full",style:{boxShadow:"chat_dashboard"===j?"0px 0px 9px 0px #c1c0c080":"unset"},children:(0,n.jsx)(Y,{clearIntialMessage:async()=>{await d()},dbList:null==w?void 0:w.data,runDbList:Z,supportTypes:null==N?void 0:N.data,isChartChat:"chat_dashboard"===j,messages:S||[],onSubmit:k,paramsList:null==P?void 0:P.data,runParamsList:C,setChartsData:l})})})]})}},57931:function(e,l,t){"use strict";t.d(l,{ZP:function(){return d},Cg:function(){return r}});var n=t(9268),i=t(89081),a=t(78915),s=t(86006);let[r,o]=function(){let e=s.createContext(void 0);return[function(){let l=s.useContext(e);if(void 0===l)throw Error("useCtx must be inside a Provider with a value");return l},e.Provider]}();var d=e=>{let{children:l}=e,{run:t,data:s,refresh:r}=(0,i.Z)(async()=>await (0,a.Tk)("/v1/chat/dialogue/list"),{manual:!0});return(0,n.jsx)(o,{value:{dialogueList:s,queryDialogueList:t,refreshDialogList:r},children:l})}},78915:function(e,l,t){"use strict";t.d(l,{Tk:function(){return c},Kw:function(){return u},PR:function(){return h},Ej:function(){return x}});var n=t(21628),i=t(24214),a=t(52040);let s=i.Z.create({baseURL:a.env.API_BASE_URL});s.defaults.timeout=1e4,s.interceptors.response.use(e=>e.data,e=>Promise.reject(e));var r=t(84835);let o={"content-type":"application/json"},d=e=>{if(!(0,r.isPlainObject)(e))return JSON.stringify(e);let l={...e};for(let e in l){let t=l[e];"string"==typeof t&&(l[e]=t.trim())}return JSON.stringify(l)},c=(e,l)=>{if(l){let t=Object.keys(l).filter(e=>void 0!==l[e]&&""!==l[e]).map(e=>"".concat(e,"=").concat(l[e])).join("&");t&&(e+="?".concat(t))}return s.get("/api"+e,{headers:o}).then(e=>e).catch(e=>{n.ZP.error(e),Promise.reject(e)})},u=(e,l)=>{let t=d(l);return s.post("/api"+e,{body:t,headers:o}).then(e=>e).catch(e=>{n.ZP.error(e),Promise.reject(e)})},h=(e,l)=>(d(l),s.post(e,l,{headers:o}).then(e=>e).catch(e=>{n.ZP.error(e),Promise.reject(e)})),x=(e,l)=>s.post(e,l).then(e=>e).catch(e=>{n.ZP.error(e),Promise.reject(e)})}},function(e){e.O(0,[180,757,282,838,60,759,192,86,316,790,767,259,751,320,253,769,744],function(){return e(e.s=83738)}),_N_E=e.O()}]);