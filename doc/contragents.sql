create or replace function USIOSMCONTRAGENT
return DummyTypeHolder.TRefCursor
is
    vSQL varchar2(4000);
    vResult DummyTypeHolder.TRefCursor;
begin
    vSQL :=
    'select c.id'||
          ',c.Name'||
          ',c.inn'||
    ' from SMClientInfo c'||
    ' where c.Accepted=1';

    open vResult for vSQL;
    return vResult;
end;
/
