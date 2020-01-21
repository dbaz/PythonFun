import os
import functools

##########################################

validationSteps = []

def addValidationDependency(*validatorFuncs):

    def wrapper(wrappedFunc):

        @functools.wraps(wrappedFunc)
        def innerValidator(*args, **kwargs):
            capturedCo = wrappedFunc.__code__.co_varnames[:wrappedFunc.__code__.co_argcount]
            # get all the args passed to the wrapped function
            kwargs.update(dict(zip(capturedCo, args)))
            if 'dryRun' in kwargs and kwargs['dryRun'] is True:
                for validatorFunc in validatorFuncs:
                    matchedParams = {k: kwargs[k] for k in validatorFunc.__code__.co_varnames if k in capturedCo}

                    # record the matched params
                    validationSteps.append((validatorFunc, matchedParams, wrappedFunc.__name__))

            # call the original function
            return wrappedFunc(**kwargs)

        return innerValidator
    return wrapper

##########################################
def validateOutPathExists(outPath):
    if outPath:
        return True, "validateOutPathExists: Shit's Worked yo"
    else:
        return False, "Shit's broke yo"

def validateIpaPath(outPath):
    if outPath:
        return True, "validateOutPathExists: Ipa Worked yo"
    else:
        return False, "Ipa Shits broke yo"

##########################################
@addValidationDependency(validateIpaPath)
def findStagingIpa(outPath, someUnusedVariable=False):
    return outPath is not None

@addValidationDependency(validateOutPathExists)
def uploadAllContent(reviewContent, fullContent):
    pass

@addValidationDependency(validateOutPathExists, validateIpaPath)
def buildCode(outPath, buildIpa, someotherBool, dryRun=False):
    someInnerVariable = 1
    someOtherVariable = "testLocalVariable"

##########################################

def pushToProduction(buildIpa, uploadReviewContent, uploadFullContent, outPath, dryRun=False):
    buildCode(outPath, buildIpa, False, dryRun)
    #uploadAllContent(uploadReviewContent, uploadFullContent)
    #ipa = findStagingIpa("/cats/are/cute", dryRun=False)
    return 1

##########################################

def validate(validationSteps):
    for func,  kwargs, calledFrom in validationSteps:
        didPass, msg = func(**kwargs)
        print("didPass '{}' msg '{}' calledFrom '{}' ".format(didPass, msg, calledFrom))

##########################################

def main():
    print("Calling stuff")
    buildIpa = True
    uploadReviewContent = True
    uploadFullContent = True
    outPath = "./test_folders/build_directory"
    pushToProduction(buildIpa, uploadReviewContent, uploadFullContent, outPath, dryRun=True)

    print("validation steps ", validationSteps)
    validate(validationSteps)

if __name__ == "__main__":
    main()