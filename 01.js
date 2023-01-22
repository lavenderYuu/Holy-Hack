var countryName = new Array("America", "Greece", "Britain", "Canada", "China", "Egypt"); 
var count=0;
//打印输出信息:
document.write("在以下字符中：<br/>");
for(var i=0; i < countryName.length; i++)
    document.write(countryName[i] + "<br/>");

//计算字符中包含a或者A的字符的个数
for(var i=0; i < countryName.length; i++){
    if(countryName[i].indexOf('A') !=-1 || countryName[i].indexOf('a') !=-1)
        count++;
}
document.write("共有" + count + "个字符中包含a或者A。");