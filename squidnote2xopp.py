#!/usr/bin/python3
"""
Program to convert SquidNote documents to Xournal++ format compressed XML files
   Run "squidnote2xopp -h" for usage information
Version 1.0.0 (2023-05-22)
Copyright (c) 2023, ZJ Laczik    
Please submit suggestions, feature requests and bug reports on https://github.com/laczik
"""

quiet = False

########################################
def import_libraries() :
	"""
	List all reuired libraries below either as "library_name" or as
	"(library_name, short_name)" tuple. This function will try
	to import the libraries listed and will print a summary error
	message and exit if any of the library imports fail.
	"""
	named_libs = [
		'sys',
		'io',
		'inspect',
		're',
		'struct',
		'datetime',

		'tempfile',
		'shutil',
		'sqlite3',
		'gzip',
		'zipfile',
		'base64',
		
		('numpy', 'np'),
		'cv2',
		#'exif',

		'argparse',

		('squidnote_page_pb2',	'SNP')
	]
	try :
		from importlib import import_module
		for named_lib in named_libs:
			if isinstance(named_lib, str) :
				lib = import_module( named_lib )
				globals()[named_lib] = lib

			elif isinstance(named_lib, tuple) :
				lib = import_module( named_lib[0] )
				globals()[named_lib[1]] = lib
	except :
		# N.B. we may not yet be able to use mprint...
		try :
			print( '\n', CRED, sys.exc_info(), CEND )
		except :
			print( '\n', CRED, '(<class \'ModuleNotFoundError\'>, ModuleNotFoundError("No module named \'sys\'") ', CEND )
		
		print( CRED, '\n\tCould not import one of the required libraries as indicated above', CEND )
		print( CRED, '\tUse pip or the package manager of your operating system to install the missing library\n', CEND )
		exit()
		
########################################

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CGREY    = '\33[90m'
CRED = CRED2       = '\33[91m'
CGREEN = CGREEN2   = '\33[92m'
CYELLOW = CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

def mprint( *args, **kwargs) :
	"""
	print messages to stderr with optional colour specified
	wrapper for print( *args, **kwargs)
	"""
	try	:
		colour = kwargs['colour']
		del kwargs['colour']
	except KeyError :
		colour = CWHITE

	if not quiet :
		print( datetime.datetime.now(), ' ', colour, file=sys.stderr, end='' )
		print( *args, **kwargs, file=sys.stderr, end='' )
		print( CEND, file=sys.stderr )

########################################
def split_colour_channels( i ) :
	"""
	get RGBA colour components from protobuf colour representation (uint32)
	
	uint32					i				protobuf colour
	(byte,byte,byte,byte)	( r,g,b,a )		RGBA tuple
	"""
	( a,r,g,b ) = struct.pack( ">I", i )
#	return struct.unpack( "<I", struct.pack( ">I", i ) )[0]
	return ( r,g,b,a )

########################################
def get_page_and_pdf_ids( sn ) :
	"""
	deserialise (parse) protobuf page description into an SN_Page object
	
	ZipFile				sn				squidnote ZIp archive handle

	[tuple(str,str)]	query_result	array of (page_id,pdf_id) tuples
	"""

	with tempfile.TemporaryDirectory() as dirpath :
		sn.extract( 'note.db', dirpath )
		db_path = dirpath + '/note.db'
		conn = sqlite3.connect(db_path)
		mprint( f'Connected to sqlite3 database {db_path}', colour=CGREEN )
		cur = conn.cursor()
		cur.execute( "SELECT id, documentId FROM page ORDER BY pageNum ASC" )
		query_result = cur.fetchall()
		mprint( f'Page / PDF ID query completed, found {len(query_result)} pages' )
		conn.close()
		mprint( f'Closed database connection' )
	return query_result


#
#with sn.open('note.db', 'r') as f_in:
#	with open('/tmp/tttt.db', 'wb') as f_out:
#		shutil.copyfileobj(f_in, f_out)
#		f_out.close()
#	f_in.close()
#
#dirpath = tempfile.mkdtemp()
## ... do stuff with dirpath
#shutil.rmtree(dirpath)
#
#sn_files = sn.namelist()
#re_pattern = re.compile( 'data/pages/.+\.page' )
#sn_pages = list(filter(re_pattern.search, sn_files))
#
#mprint( sn_files )
#mprint( sn_pages )
#
#	members = [attr for attr in dir( page ) if not callable( getattr( page, attr ) ) and not attr.startswith( "__" )]
#	members = [attr for attr in dir( page )]
#	print( members )
#	print( page.UnknownFields( ) )
#	print( page.ListFields( ) )

########################################
def parse_page_file( sn, page_id ) :
	"""
	deserialise (parse) protobuf page description into an SN_Page object
	
	ZipFile		sn			squidnote ZIp archive handle
	string		page_id		name of the protobuf page file stored in the squidnote ZIP archive
	
	int			ret_val		number of items parsed
	SN_Page		SN_Page		object containing all page components
	"""

	name = 'data/pages/' + page_id + '.page'

	page = SNP.SN_Page( )
	mprint( 'Created page protocol buffer' )
	
	with sn.open( name, "r" ) as fd :
		mprint( f'Opened page file {name}', colour=CGREEN )
		ret_val = page.ParseFromString( fd.read( ) )
		fd.close()
		mprint( f'Closed page file' )
		
	return (ret_val, page)

########################################
def check_for_unknown_fields( msg, indt='>>' ) :
	"""
	Traverse all fields in protobuf message
	and check for unknown fields
	"""	

#	ukf = msg.UnknownFields
	ukf = msg._unknown_fields
	print( '+++++', type( ukf ) )

	print( dir( msg ) )
	
	
	for (field_descriptor, value) in msg.ListFields() :
		try :
#			for di in dir( field_descriptor ) :
#			for di in dir( value ) :
#				print( di )

			print( indt , field_descriptor.name  )
			if field_descriptor.label is field_descriptor.LABEL_REPEATED :
				for fd in value :
					check_for_unknown_fields( fd, indt+'    ' )
			elif field_descriptor.type is field_descriptor.TYPE_MESSAGE :
				check_for_unknown_fields( value, indt+'    ' )
#			else :
#				print( indt+'    ', type( value ) )
		except  Exception as e :
			print( '********** error' )
			print( e )
			pass

########################################
def generate_xournal_xml_doc( sn, xopp_doc, xopp_file, dry_run, stroke_scale, highlight_scale, image_dpi ) :
	"""
	- extract page and PDF IDs from squidnote sqlite3 database
	- extract and save all PDF background files frm squidnote ZIp archive
	- cycle over page IDs and generate page XML sections
	- for each page cycle over layer / item / etc specifications in protobuf page files
		and generate corresponding XML components
		
	ZipFile		sn			squidnote ZIp archive handle
	StringIO	xopp_doc	buffer for collecting XML bits
	string		xopp_file	xopp document filename (used for naming background PDFs
	bool		dry_run		do not write any files when set
	"""
	# extract page and pdf background IDs from sqlite3 database
	page_and_pdf_ids = get_page_and_pdf_ids(sn)

	# extract all PDFs from squidnote ZIP archive to separate files
	# only keep pdf_ids at index 1 in each tuple
	pdf_ids = list( set( [ a[1] for a in page_and_pdf_ids ] ) )
	# cycle over all PDF file entries
	if not dry_run :
		for pdf_id in pdf_ids :
			if pdf_id :
				try :
					src = "data/docs/" + pdf_id
					dest = xopp_file + '.' + pdf_id + '.pdf'
					sn.getinfo(src).filename = dest
					sn.extract(src)
					mprint( f'Extracted background PDF from "data/docs" to "{dest}"', colour=CGREEN )
				except :
					mprint( f'Failed to extract background PDF from "data/docs" to "{dest}"', colour=CRED )
				
	# generate XML header
	mprint( 'Starting XML page description generation' )
	xopp_doc.write( '<?xml version="1.0" standalone="no"?>' )
	xopp_doc.write( '<xournal creator="Xournal++ 1.1.1" fileversion="4">' )
	xopp_doc.write( '<title>Xournal++ document - see https ://github.com/xournalpp/xournalpp</title>' )

	# cycle over all pages as listed in the squidnote database (retrieved above)
	for page_number, (page_id, pdf_id) in enumerate( page_and_pdf_ids ) :

		# generate <page> section of the XML file
		mprint( f'Generating XML page description for page {page_number:d}' )

		# extract from ZIP archive and parse page file for current page
		ret_val, page = parse_page_file( sn, page_id )
		mprint( f'Parsed {ret_val} objects for page {page_number}', colour=CGREEN )

		# check that our protocol buffer specification is correct and we are not missing any fields
#		check_for_unknown_fields( page )

		# generate page background section of XML file
		match page.background.type :
			case SNP.SN_BT_BLANK :
				w = 28.34645669 * page.background.width
				h = 28.34645669 * page.background.height
				r,g,b,a = split_colour_channels( page.background.colour )

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
				xopp_doc.write( f'<background type="solid" color="#{r:02x}{g:02x}{b:02x}{a:02x}" style="plain"/>' )
			case SNP.SN_BT_UNDEFINED :
				mprint( f'Page background type {page.background.type} (SN_BT_UNDEFINED) replaced by blank background', colour=CYELLOW )
				w = 28.34645669 * page.background.width
				h = 28.34645669 * page.background.height
				r,g,b,a = split_colour_channels( page.background.colour )

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
				xopp_doc.write( f'<background type="solid" color="#{r:02x}{g:02x}{b:02x}{a:02x}" style="plain"/>' )
			case SNP.SN_BT_RULEDPAPER :
				mprint( f'Page background type {page.background.type} (SN_BT_RULEDPAPER) replaced by blank background', colour=CYELLOW )
				w = 28.34645669 * page.background.width
				h = 28.34645669 * page.background.height
				r,g,b,a = split_colour_channels( page.background.colour )

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
				xopp_doc.write( f'<background type="solid" color="#{r:02x}{g:02x}{b:02x}{a:02x}" style="plain"/>' )
			case SNP.SN_BT_QUADPAPER :
				mprint( f'Page background type {page.background.type} (SN_BT_QUADPAPER) replaced by blank background', colour=CYELLOW )
				w = 28.34645669 * page.background.width
				h = 28.34645669 * page.background.height
				r,g,b,a = split_colour_channels( page.background.colour )

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
				xopp_doc.write( f'<background type="solid" color="#{r:02x}{g:02x}{b:02x}{a:02x}" style="plain"/>' )
			case SNP.SN_BT_PDF :
				w = 28.34645669 * page.background.width
				h = 28.34645669 * page.background.height
				r,g,b,a = split_colour_channels( page.background.colour )
				pn = page.background.pdf.page_number + 1

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
# it seems xournal wants the filename specified in each <page> entry...
#				if pn == 1 :
				xopp_doc.write( f'<background type="pdf" domain="attach" filename="{pdf_id}.pdf" pageno="{pn}"/>' )
#				else :
#					xopp_doc.write( f'<background type="pdf" pageno="{pn}"/>' )
			case SNP.SN_BT_PAPYR :
				mprint( f'Page background type {page.background.type} (SN_BT_PAPYR) replaced by blank background', colour=CYELLOW )
				w = 28.34645669 * page.background.width
				h = 28.34645669 * page.background.height
				r,g,b,a = split_colour_channels( page.background.colour )

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
				xopp_doc.write( f'<background type="solid" color="#{r:02x}{g:02x}{b:02x}{a:02x}" style="plain"/>' )
			case _ :
				mprint( f'Unhandled unknown page background type {page.background.type} replaced by A4 background' , colour=CYELLOW)
				w = 28.34645669 * 21.0
				h = 28.34645669 * 29.7
				r,g,b,a = ( 0xff, 0xff, 0xff, 0xff )

				xopp_doc.write( f'<page width="{w:.3f}" height="{h:.3f}">' )
				xopp_doc.write( f'<background type="solid" color="#{r:02x}{g:02x}{b:02x}{a:02x}" style="plain"/>' )

		# generate <layer> section(s) of the XMl file
		for il, lr in enumerate( page.layer ) :
			xopp_doc.write( '<layer>' )
			for ii, im in enumerate( lr.item ) :
				match im.type :
					case SNP.SN_Item_Type.SN_IT_STROKE :
						match im.stroke.type :
							case SNP.SN_Stroke_Type.SN_ST_NORMAL :
								r,g,b,a = split_colour_channels( im.stroke.colour )
								xopp_doc.write( f'<stroke tool="pen" ts="0" fn="" color="#{r:02x}{g:02x}{b:02x}{a:02x}"' )
								w = stroke_scale * 2.834645669 * im.stroke.weight
								xopp_doc.write( f' width="{w:.3f}' )
								for pt in im.stroke.delta :
									w = stroke_scale * 2.834645669 * pt.weight
									xopp_doc.write( f' {w:.3f}' )
								xopp_doc.write( '">' )
								ref_x = 28.34645669 * im.stroke.start.x
								ref_y = 28.34645669 * im.stroke.start.y
								xopp_doc.write( f'{ref_x:.3f} {ref_y:.3f}' )
								for pt in im.stroke.delta :
									x = ref_x + 28.34645669 * pt.dx
									y = ref_y + 28.34645669 * pt.dy
									xopp_doc.write( f' {x:.3f} {y:.3f}' )
								xopp_doc.write( '</stroke>\n' )
							case SNP.SN_Stroke_Type.SN_ST_HIGHLIGHT :
								r,g,b,a = split_colour_channels( im.stroke.colour )
								xopp_doc.write( f'<stroke tool="highlighter" ts="0" fn="" color="#{r:02x}{g:02x}{b:02x}{a:02x}"' )
								w = highlight_scale * 28.34645669 * im.stroke.weight
								xopp_doc.write( f' width="{w:.3f}' )
								for pt in im.stroke.delta :
									w = highlight_scale * 28.34645669 * pt.weight
									xopp_doc.write( f' {w:.3f}' )
								xopp_doc.write( '">' )
								ref_x = 28.34645669 * im.stroke.start.x
								ref_y = 28.34645669 * im.stroke.start.y
								xopp_doc.write( f'{ref_x:.3f} {ref_y:.3f}' )
								for pt in im.stroke.delta :
									x = ref_x + 28.34645669 * pt.dx
									y = ref_y + 28.34645669 * pt.dy
									xopp_doc.write( f' {x:.3f} {y:.3f}' )
								xopp_doc.write( '</stroke>\n' )
							case SNP.SN_Stroke_Type.SN_ST_UNDEFINED :
								mprint( f'Unhandled stroke type {im.stroke.type} (SN_ST_UNDEFINED)', colour=CYELLOW )
							case SNP.SN_Stroke_Type.SN_ST_LINE :
								mprint( f'Unhandled stroke type {im.stroke.type} (SN_ST_LINE)', colour=CYELLOW )
							case SNP.SN_Stroke_Type.SN_ST_SMOOTH :
								mprint( f'Unhandled stroke type {im.stroke.type} (SN_ST_SMOOTH)', colour=CYELLOW )
							case _  :
								mprint( f'Unhandled unknown stroke type {im.stroke.type}' )
					case SNP.SN_Item_Type.SN_IT_UNDEFINED :
						mprint( f'Unhandled item type {im.type} (SN_IT_UNDEFINED) at position {il}', colour=CYELLOW )
					case SNP.SN_Item_Type.SN_IT_SHAPE :
						mprint( f'Unhandled item type {im.type} (SN_IT_SHAPE) at position {il}', colour=CYELLOW )
					case SNP.SN_Item_Type.SN_IT_TEXT :
						mprint( f'Unhandled item type {im.type} (SN_IT_TEXT) at position {il}', colour=CYELLOW )
					case SNP.SN_Item_Type.SN_IT_IMAGE :
						cl = im.image.crop_bounds.left
						cr = im.image.crop_bounds.right
						ct = im.image.crop_bounds.top
						cb = im.image.crop_bounds.bottom

						l = 28.34645669 * im.image.bounds.left
						r = 28.34645669 * im.image.bounds.right
						t = 28.34645669 * im.image.bounds.top
						b = 28.34645669 * im.image.bounds.bottom

						xopp_doc.write( f'<image left="{l:.3f}" top="{t:.3f}" right="{r:.3f}" bottom="{b:.3f}">\n' )

						name = 'data/imgs/' + im.image.image_hash 
						with sn.open( name, "r" ) as fd :
							img = fd.read()
							fd.close()

						npimg = np.asarray( bytearray(img), dtype=np.uint8)
						# use IMREAD_UNCHANGED instead of IMREAD_COLOR to ignore EXIF orientation (as does squidnote)
						cvimg = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)

						cvimg = cvimg[ct:cb, cl:cr]
						if im.image.flip_x :
							cvimg = cv2.flip( cvimg, 0 )
						if im.image.flip_y :
							cvimg = cv2.flip( cvimg, 1 )
						match im.image.rotation :
							case 90 :
								cvimg = cv2.rotate( cvimg, cv2.ROTATE_90_CLOCKWISE )
							case 180 :
								cvimg = cv2.rotate( cvimg, cv2.ROTATE_180 )
							case 270 :
								cvimg = cv2.rotate( cvimg, cv2.ROTATE_90_COUNTERCLOCKWISE )
							case _ :
								mprint( f'Image rotation angle {im.image.rotation} is not supported', colour=CYELLOW )
						# image_dpi
						current_x_dpi = 72.0 * (cr-cl) / (r-l)
						current_y_dpi = 72.0 * (cb-ct)/(b-t)
						x_scale = min( 1.0, image_dpi / current_x_dpi )
						y_scale = min( 1.0, image_dpi / current_y_dpi )

#						print( x_scale, y_scale )

						cvimg = cv2.resize( cvimg, None, fx=x_scale, fy=y_scale )
#						cvimg = cv2.resize( cvimg, None, fx=0.1, fy=0.1 )
						enc_img = cv2.imencode('.png', cvimg)
						b64_string = base64.encodebytes( enc_img[1]).decode('utf-8' )

						xopp_doc.write( b64_string )
						xopp_doc.write( '</image>\n' )
						mprint( f'Inserted image from file {name}' )

					case _ :
						mprint( f'Unhandled unknown item type {im.type} at position {il}', colour=CYELLOW )

			xopp_doc.write( '</layer>\n' )
			mprint( f'Completed page {page_number} / layer {il}', colour=CGREEN )

		xopp_doc.write( '</page>\n' )
		mprint( f'Completed XML generation for page {page_number}', colour=CGREEN )

	xopp_doc.write( '</xournal>' )
	mprint( 'Completed XML generation for document', colour=CGREEN )

########################################
def main( ) :
	"""
	This is the "main" function
	"""
	global quiet

	# programmatically import all libraries listed at the top
	import_libraries()

	# process command line arguments
	parser = argparse.ArgumentParser(
		description='Convert Squid Note files to Xournal++ format',
		epilog='Please submit buf reports on GitHub (link to be provided)'
		)

	parser.add_argument( "-f", "--filename",		action='store',			help='Input/output file base name', 	required=True )
	parser.add_argument( "-s", "--stroke-scale",	action='store',			help='Scale stroke width [1.0]', 		default=1.0, type=float )
	parser.add_argument( "-l", "--highlight-scale",	action='store',			help='Scale highlight width [1.0]',		default=1.0, type=float )
	parser.add_argument( "-d", "--image-dpi",		action='store',			help='DPI for embedded images [150]',	default=150, type=int )
	parser.add_argument( "-x", "--xml",				action='store_true',	help='Generate XML file [false]' )
	parser.add_argument( "-n", "--dry-run",			action='store_true',	help='Do not write any files [false]' )
	parser.add_argument( "-v", "--version",			action='store_true',	help='About' )
	parser.add_argument( "-q", "--quiet",			action='store_true',	help='Disable progress reporting [false]' )

	args = parser.parse_args()

	if args.version :
# this is not needed, parent's __doc__ is used automatically
#		frm = inspect.stack()[1]
#		mod = inspect.getmodule(frm[0])
#		print( f'{mod.__doc__}')
		print( __doc__ )
		exit()

	quiet = args.quiet
	if args.dry_run :
		mprint( f'This is a dry run, no files will be written', colour=CYELLOW )
	sn_file = args.filename
	mprint( f'Input file:  "{sn_file}"', colour=CGREEN )
	xopp_file = args.filename + '.xopp' 
	mprint( f'Output file: "{xopp_file}"' )
	xopp_xml_file = args.filename + '.xml.xopp' 
	mprint( f'XML file:    "{xopp_xml_file}"' )

	# create buffer for building XML doc in
	xopp_doc = io.StringIO( )
	mprint( 'Created io.StringIO buffer xopp_doc' )

	# open squidnote document archive as ZipFile object
	sn = zipfile.ZipFile( sn_file, 'r' )
	mprint( f'Opened squidnote document archive "{sn_file}"' )

	# call to generate XML components
	generate_xournal_xml_doc(sn, xopp_doc, xopp_file, args.dry_run, args.stroke_scale, args.highlight_scale, args.image_dpi)

	if not args.dry_run :
		# save gzip compressed Xournal++ document
		with gzip.open( xopp_file, 'wb' ) as f :
			mprint( f'Opened Xournal++ file "{xopp_file}"' )
			f.write( xopp_doc.getvalue( ).encode( ) )
			mprint( f'Wrote Xournal++ file', colour=CGREEN )
			f.close( )
			mprint( f'Closed Xournal++ file' )

		if args.xml :
			# save uncompressed XML Xournal++ document
			with open( xopp_xml_file, 'wb' ) as f :
				mprint( f'Opened Xournal++ XML file "{xopp_xml_file}"' )
				f.write( xopp_doc.getvalue( ).encode( ) )
				mprint( f'Wrote Xournal++ XML file', colour=CGREEN )
				f.close( )
				mprint( f'Closed Xournal++ file' )

	# close open StrinIO and ZipFile
	xopp_doc.close( )
	mprint( 'Closed io.StringIO buffer xopp_doc' )
	sn.close()
	mprint( f'Closed squidnote document archive "{sn_file}"' )

	# we are done
	mprint( f'Finished', colour=CGREEN )

########################################
if __name__ == "__main__":
	main()

