# Rules

Following are the identifier naming rules supported by this tool:

 - [Non-Verb Starting Term](#non-verb-starting-term)
 - [Test Annotation](#test-annotation)
 - [Before Annotation](#before-annotation)
 - [After Annotation](#after-annotation)

## Non-Verb Starting Term

### Applicability

 - Identifier Type: Method
 - File Type: Test
 - JUnit Version: N/A

The starting term of the method's name must be a verb. If the starting term is 'test', then the rule checks if the second term is a verb.

### Example

The following test method name is a violation of the rule:

    @Test
    @EnabledOnOs({OS.WINDOWS})
    public void testProductionFileNameWindows() {
        String oracle = "Graph.java";
        String output = testFileWindows.getProductionFileName();
        assertEquals(oracle, output);
    }

The following test method name is ***not*** a violation of the rule:

    @Test
    @EnabledOnOs({OS.LINUX, OS.MAC})
    public void testGetFileNameUnix() {
        String oracle = "RandomStringUtilsTest.java";
        String output = testFileUnix.getTestFileName();
        assertEquals(oracle, output);
    }
**[*[↑](#rules)*]**

## Test Annotation 

### Applicability

 - Identifier Type: Method
 - File Type: Test
 - JUnit Version: 4+

The starting term of the test method's name should not be 'test'; annotate the method using the `@Test` annotation. 

### Example

The following test method name is a violation of the rule:

    @Test
    @EnabledOnOs({OS.WINDOWS})
    public void testProductionFileNameWindows() {
        String oracle = "Graph.java";
        String output = testFileWindows.getProductionFileName();
        assertEquals(oracle, output);
    }

The following test method name is ***not*** a violation of the rule:

    @Test
    public void deleteAllFiresClearEvent() {
	    assertThat(regionClearListener.eventFired).isFalse();
	    repository.deleteAll();
	    assertThat(regionClearListener.eventFired).isTrue();
    }
**[*[↑](#rules)*]** 

## Before Annotation

### Applicability

 - Identifier Type: Method
 - File Type: Test
 - JUnit Version: 4+

A method with the name 'setup' must use `@Before` annotation.

### Example

The following test method name is a violation of the rule:

        public void setUp(Context c) {
            mCursor = c.getContentResolver().query(People.CONTENT_URI, PEOPLE_PROJECTION, null,
                    null, People.DEFAULT_SORT_ORDER);
        }

The following test method name is ***not*** a violation of the rule:

    @Before
    public void setup() throws Exception {
        this.mojo = new AbstractGitMojo() {
            public void run()
                    throws MojoExecutionException {}
        };

        super.setup();
        this.mojo.init();
    }
**[*[↑](#rules)*]** 

## After Annotation

### Applicability

 - Identifier Type: Method
 - File Type: Test
 - JUnit Version: 4+

A method with the name 'teardown' must use `@After` annotation.

### Example

The following test method name is a violation of the rule:

      @Override protected void tearDown() {
		  tearDownStack.runTearDown();
      }


The following test method name is ***not*** a violation of the rule:

    @After
    public void tearDown() {
	    if (this.mojo != null) {
            this.mojo.cleanup();
        }
    }
**[*[↑](#rules)*]** 


##### [Back To ReadMe](../../README.md)