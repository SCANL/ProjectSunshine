# Naming Violation Examples



[TOC]



## "Get" more than accessor

**Id:**  A.1

**Description:** A getter that performs actions other than returning the corresponding attribute.

**Example:**

```java
public Set<Cloud> getClouds() {
    if(clouds==null) {
        Set<Cloud> r = new HashSet<>();
        Jenkins h = Jenkins.get();
        for (Cloud c : h.clouds) {
            if(c.canProvision(this))
                r.add(c);
        }
        clouds = Collections.unmodifiableSet(r);
    }
    return clouds;
}
```

**Explanation:** This is a getter method as it returns an attribute (i.e., `clouds`). However, in addition to returning the attribute, the method also contains conditional statements (i.e., if checks and for loop). A getter method should not manipulate the attribute.

**Source:** https://github.com/jenkinsci/jenkins/blob/180de86abb6ff02f45f10f676d3d358a81dc95c8/core/src/main/java/hudson/model/Label.java#L253



## "Is" returns more than a Boolean

**Id:** A.2

**Description:** The name of a method is a predicate suggesting a true/false value in return. However the return type is not Boolean but rather a more complex type.

**Example:**

```C#
internal static Expression IsStrictMode(int version, Expression executionContext = null)
{
	if (executionContext == null)
    {
    	executionContext = ExpressionCache.NullExecutionContext;
   	}

    return Expression.Call(
    	CachedReflectionInfo.ExecutionContext_IsStrictVersion,
        executionContext,
        ExpressionCache.Constant(version));
}
```

**Explanation:** In this example, the method name starts with the term "Is", a predicate term, which means that the method should either return true or false. However, the return type is a custom complex type.

**Source:** https://github.com/PowerShell/PowerShell/blob/ea5c8e3c4dfa002e74e7e3d81f5ca489daf3f097/src/System.Management.Automation/engine/parser/Compiler.cs#L1103



## "Set" method returns

**Id:** A.3

**Description:** A set method having a return type different than void.

**Example:**

```java
public static String setCurrentDescriptorByNameUrl(String value) {
    String o = getCurrentDescriptorByNameUrl();
    Stapler.getCurrentRequest().setAttribute("currentDescriptorByNameUrl", value);

    return o;
}
```

**Explanation:** The purpose of setter methods is to assign values and do not return anything. In this example, the method returns a string. 

**Source:** https://github.com/jenkinsci/jenkins/blob/180de86abb6ff02f45f10f676d3d358a81dc95c8/core/src/main/java/hudson/Functions.java#L2177



## Expecting but not getting a single instance

**Id:** A.4

**Description:** The name of a method indicates that a single object is returned but the return type is a collection.

**Example:**

```C#
internal override PSObject[] GetParameter(string pattern)
{
	return _helpInfo.GetParameter(pattern);
}
```

**Explanation:** This method returns a collection (i.e., array) of objects (specifically, `PSObject`). However, the last term in the method name is singular (i.e., "Parameter"). This inconsistency is a linguistic anti-pattern.

**Source:** https://github.com/PowerShell/PowerShell/blob/ea5c8e3c4dfa002e74e7e3d81f5ca489daf3f097/src/System.Management.Automation/help/ProviderCommandHelpInfo.cs#L46



## Not implemented condition

**Id:** B.1

**Description:** The comments of a method suggest a conditional behavior that is not implemented in the code. When the implementation is default this should be documented.

**Example:**

```java
/**
 * Returns a {@link Converter} for converting {@code type} to an HTTP request body, or null if
 * {@code type} cannot be handled by this factory. This is used to create converters for types
 * specified by {@link Body @Body}, {@link Part @Part}, and {@link PartMap @PartMap} values.
 */
public @Nullable Converter<?, RequestBody> requestBodyConverter(
    Type type,
    Annotation[] parameterAnnotations,
    Annotation[] methodAnnotations,
    Retrofit retrofit) {
  return null;
}
```

**Explanation:** In this example, the method comment indicates that the method checks for a condition (i.e., "...or null if..."). However, the method body does not contain any conditional statements.

**Source:** https://github.com/square/retrofit/blob/bd33a5da186aa6f5365e78e27eb0292b1b8b1bff/retrofit/src/main/java/retrofit2/Converter.java#L63



## Validation method does not confirm

**Id:** B.2

**Description:** A validation method (e.g., name starting with validate, check, ensure) does not confirm the validation, i.e., the method neither provides a return value informing whether the validation was successful, nor documents how to proceed to understand.

**Example:**

```C#
private void CheckClose()
{
	if (_connectionShutdown && _remoteShutdown)
    {
    	Close();
    }
}
```

**Explanation:** In this method, the starting term (i.e., "Check") indicates that this method should perform some form of validation. Such methods should return the result of the check, which is either true or false. However, in this case, this method does not return any value.

**Source:** https://github.com/shadowsocks/shadowsocks-windows/blob/ac0fcdfc8c615d62e56a30c9583e3dca51ff93d4/shadowsocks-csharp/Controller/Service/TCPRelay.cs#L283



## "Get" method does not return

**Id:** B.3

**Description:** The name suggests that the method returns something (e.g., name starts with get or return) but the return type is void.

**Example:** The first term in this method (i.e., "Get") indicates that this method should be returning a value. However, this method does not return anything.

```C#
public static void GetBytes(byte[] buf, int len)
{
	if (_rng == null) Init();
    try
    	{
        	_rng.GetBytes(buf, 0, len);
        }
	catch
    {
    	// the backup way
        byte[] tmp = new byte[len];
        _rng.GetBytes(tmp);
        Buffer.BlockCopy(tmp, 0, buf, 0, len);
    }
}
```

**Explanation:** 

**Source:** https://github.com/shadowsocks/shadowsocks-windows/blob/ac0fcdfc8c615d62e56a30c9583e3dca51ff93d4/shadowsocks-csharp/Encryption/RNG.cs#L32



## Not answered question

**Id:** B.4

**Description:** The name of a method is in the form of predicate whereas the return type is not Boolean.

**Example:**

```C#
private void IsDisposed()
{
	if (_isDisposed == true)
    {
    	string msg = StringUtil.Format(ScheduledJobErrorStrings.DefinitionObjectDisposed, Name);
        throw new RuntimeException(msg);
    }
}
```

**Explanation:** The method name starts with a predicate (i.e., "Is") and is supposed to return either true or false. However, this method does not return a boolean value. 

**Source:** https://github.com/PowerShell/PowerShell/blob/ea5c8e3c4dfa002e74e7e3d81f5ca489daf3f097/src/Microsoft.PowerShell.ScheduledJob/ScheduledJobDefinition.cs#L555



## Transform method does not return

**Id:** B.5

**Description:** The name of a method suggests the transformation of an object but there is no return value and it is not clear from the documentation where the result is stored.

**Example:**

```java
public void translate(String markup, @NonNull Writer output) throws IOException {
	Matcher m = Pattern.compile("[<>]").matcher(markup);
    StringBuffer buf = new StringBuffer();
    while (m.find()) {
    	m.appendReplacement(buf, m.group().equals("<") ? "<b>[</b>" : "<b>]</b>");
    }
    m.appendTail(buf);
    output.write(buf.toString());
}
```

**Explanation:** The term (i.e., "translate") in this method name means that the method performs data transformation. For such transformation methods, the transformed data should be returned, but in this case, the method does not return data.

**Source:** https://github.com/jenkinsci/jenkins/blob/180de86abb6ff02f45f10f676d3d358a81dc95c8/test/src/test/java/hudson/model/ParametersTest.java#L271



## Expecting but not getting a collection

**Id:** B.6

**Description:** The name of a method suggests that a collection should be returned but a single object or nothing is returned.

**Example:**

```C#
public static void GetBytes(byte[] buf)
{
	GetBytes(buf, buf.Length);
}
```

**Explanation:** The first term in this method (i.e., "Get") means that this method should return data. Furthermore, the last term in this method name (i.e., "Bytes") is plural, meaning that the returned data should be a collection. However, in this case, the method does not return a collection.

**Source:** https://github.com/shadowsocks/shadowsocks-windows/blob/ac0fcdfc8c615d62e56a30c9583e3dca51ff93d4/shadowsocks-csharp/Encryption/RNG.cs#L27



## Method name and return type are opposite

**Id:** C.1

**Description:** The documentation of a method is in contradiction with its declaration.

**Example:**

```java
private void validateServiceInterface(Class<?> service) {
	if (!service.isInterface()) {
      throw new IllegalArgumentException("API declarations must be interfaces.");
    }
```

**Explanation:** In this example, the name of the method's return type (i.e., "void") is an antonym for a term in the method's name (i.e., "validate").

**Source:** https://github.com/square/retrofit/blob/bd33a5da186aa6f5365e78e27eb0292b1b8b1bff/retrofit/src/main/java/retrofit2/Retrofit.java#L165



## Method signature and comment are opposite

**Id:** C.2

**Description:** The name of an attribute suggests a single instance, while its type suggests that the attribute stores a collection of objects.

**Example:**

```c#
/// <summary>
/// Removes and returns the specified number of objects from the beginning of the <see cref="ByteCircularBuffer"/>.
/// </summary>
/// <param name="count">The number of elements to remove and return from the <see cref="ByteCircularBuffer"/>.</param>
/// <returns>The objects that are removed from the beginning of the <see cref="ByteCircularBuffer"/>.</returns>
public byte[] Get(int count)
{
	if (count <= 0) throw new ArgumentOutOfRangeException("should greater than 0");
    var result = new byte[count];

    this.Get(result);

    return result;
}
```

**Explanation:** In this example, a term in the method's comment (i.e., "Remove") is an antonym for a term in the method's name (i.e., "Get").

**Source:** https://github.com/shadowsocks/shadowsocks-windows/blob/ac0fcdfc8c615d62e56a30c9583e3dca51ff93d4/shadowsocks-csharp/Encryption/CircularBuffer/ByteCircularBuffer.cs#L245



## Says one but contains many

**Id:** D.1

**Description:** The name of an attribute suggests a single instance, while its type suggests that the attribute stores a collection of objects.

**Example:**

```c#
private string[] computername;
```

**Explanation:** The data type of this attribute is a collection (i.e., array) of a `string` type. However, the term in the attribute's names is singular (i.e., "name"), thereby creating an inconsistency.

**Source:** https://github.com/PowerShell/PowerShell/blob/ea5c8e3c4dfa002e74e7e3d81f5ca489daf3f097/src/Microsoft.Management.Infrastructure.CimCmdlets/RemoveCimInstanceCommand.cs#L111



## Name suggests boolean but type is not

**Id:** D.2

**Description:** The name of an attribute suggests that its value is true or false, but its declaring type is not Boolean.

**Example:**

```c#
private readonly int[] _isPatternPositionVisitedMarker;
```

**Explanation:** In this example, the attribute name starts with a predicate (i.e., "is"), indicating that the attribute value should be either true or false. However, in this case, the associated type is not boolean.

**Source:** https://github.com/PowerShell/PowerShell/blob/ea5c8e3c4dfa002e74e7e3d81f5ca489daf3f097/src/System.Management.Automation/engine/regex.cs#L1008



## Says many but contains one

**Id:** E.1

**Description:** The name of an attribute suggests multiple instances, but its type suggests a single one.

**Example:**

```java
/**
 * List of lowercase names of variable that will be retained from removal
 */
private String variables = "";
```

**Explanation:** The term in the attribute's names is plural (i.e., "variables"), but the associated type is not a collection (i.e., `String`), thereby creating an inconsistency.

**Source:** https://github.com/jenkinsci/jenkins/blob/180de86abb6ff02f45f10f676d3d358a81dc95c8/core/src/main/java/jenkins/tasks/filters/impl/RetainVariablesLocalRule.java#L73



## Attribute name and type are opposite

**Id:** F.1

**Description:** The name of an attribute is in contradiction with its type as they contain antonyms.

**Example:**

```java
final FreeStyleProject restrictedProject = createLongRunningProject(TEST_JOB_NAME);
```

**Explanation:** In this example, a term in the name of the attribute's data type (i.e., "Free") is an antonym for a term in the attribute's name (i.e., "restricted").

**Source:** https://github.com/jenkinsci/jenkins/blob/180de86abb6ff02f45f10f676d3d358a81dc95c8/test/src/test/java/jenkins/cli/StopBuildsCommandTest.java#L147



## Attribute signature and comment are opposite

**Id:** F.2

**Description:** The declaration of an attribute is in contradiction with its documentation.

**Example:**

```java
// disabled by default until proven in the production
public boolean enabled = SystemProperties.getBoolean(ConnectionActivityMonitor.class.getName()+".enabled");
```

**Explanation:** In this example, a term in the name of the attribute's comment (i.e., "disabled") is an antonym for a term in the attribute's name (i.e., "enabled").

**Source:** https://github.com/jenkinsci/jenkins/blob/180de86abb6ff02f45f10f676d3d358a81dc95c8/core/src/main/java/hudson/slaves/ConnectionActivityMonitor.java#L106



## Name contains only special characters

**Id:** G.1

**Description:** The name of the identifier is composed of only non-alphanumeric characters.

**Example:**

```C#
private void HandleCreateAndInvokePowerShell(object _, RemoteDataEventArgs<RemoteDataObject<PSObject>> eventArgs)
{
	RemoteDataObject<PSObject> data = eventArgs.Data;
    .
    .
}
```

**Explanation:** In this example, the name of the parameter in the method is composed of only an underscore.

**Source:** https://github.com/PowerShell/PowerShell/blob/ea5c8e3c4dfa002e74e7e3d81f5ca489daf3f097/src/System.Management.Automation/engine/remoting/server/ServerRunspacePoolDriver.cs#L709



## Redundant use of "test" in method name 

**Id:** G.2

**Description:** The name of a test method starts with the term 'test'.

**Example:**

```java
@Test
public void test() {
	Retrofit retrofit =
    	new Retrofit.Builder()
            .baseUrl(server.url("/"))
            .addConverterFactory(new ToStringConverterFactory())
            .validateEagerly(true)
            .build();
	assertNotNull(retrofit.create(Example.class));
}
```

**Explanation:** In this example, the test method's name is "test", and the method also utilizes the @Test annotation. When using this specific annotation, it is unnecessary to start the method's name with the term "test".

**Source:** https://github.com/square/retrofit/blob/bd33a5da186aa6f5365e78e27eb0292b1b8b1bff/retrofit/src/test/java/retrofit2/Java8DefaultStaticMethodsInValidationTest.java#L44





[Back To ReadMe](../../README.md)