# Call with any argument (e.g. --force or force or blah) to force
# the script to regenerate all of the html files from source.

read -d '' prepend << EOF
<link rel="stylesheet" href="github-markdown.css">
<style>
	.markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
	}
</style>
<article class="markdown-body">
EOF

postpend="</article>"

cd entries
for i in *.md; do
    html_location=../generated_html/${i%.md}.html
    # Only generate the html if the markdown is newer (or the html no existe).
    if [ "$i" -nt "$html_location" ] || [ $1 ]; then
        python3 -m markdown -x markdown.extensions.nl2br $i > $html_location;
        tmpfile=`mktemp`
        echo $prepend | cat - $html_location > $tmpfile
        echo $postpend >> $tmpfile
        mv $tmpfile $html_location
        echo $i
    fi
done
cd ..

#python /usr/local/lib/python3.4/dist-packages/markdown2.py --extras markdown-in-html,nl2b \
#  $i > ../generated_html/$no_ext.html
