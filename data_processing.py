import data_import_and_prep_and_display as dataimport
print "Let's get data for a column in a seven column array: "
var = raw_input("Enter column (1-7): ")
prepared_var = int(var)-1
print "Header:"
print dataimport.getColumnHeader(prepared_var)

print "Content:"
print dataimport.getColumnContent(prepared_var)
