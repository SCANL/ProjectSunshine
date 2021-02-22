# Rules

Following are the identifier naming rules supported by this tool.

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


## Test Annotation

### Applicability

 - Identifier Type: Method
 - File Type: Test
 - JUnit Version: 4+

The starting term of the test method's name should not be 'test'; annotate the method using the `@Test` annotation. 

### Example

The following test method name is a violation of the rule:

    @Test
    @EnabledOnOs({OS.LINUX, OS.MAC})
    public void testGetFileNameUnix() {
        String oracle = "RandomStringUtilsTest.java";
        String output = testFileUnix.getTestFileName();
        assertEquals(oracle, output);
    }

The following test method name is ***not*** a violation of the rule:

    @Test
    public void deleteAllFiresClearEvent() {
	    assertThat(regionClearListener.eventFired).isFalse();
	    repository.deleteAll();
	    assertThat(regionClearListener.eventFired).isTrue();
    }