import { IAutoBeTypeScriptCompileResult } from "../compiler";
import {
  AutoBeTestWriteAuthorizationFunction,
  AutoBeTestWriteFunction,
  AutoBeTestWriteGenerationFunction,
  AutoBeTestWritePrepareFunction,
} from "../histories";
import { AutoBeAggregateEventBase } from "./base/AutoBeAggregateEventBase";
import { AutoBeEventBase } from "./base/AutoBeEventBase";

/**
 * Event fired when the Test agent corrects compilation failures in the
 * generated test code through the AI self-correction feedback process.
 *
 * This event occurs when the embedded TypeScript compiler detects compilation
 * errors in the test code and the Test agent receives detailed error feedback
 * to correct the issues. The correction process demonstrates the sophisticated
 * feedback loop that enables AI to learn from compilation errors and improve
 * test code quality iteratively.
 *
 * The correction mechanism ensures that test code not only compiles
 * successfully but also properly validates API functionality while maintaining
 * consistency with the established API contracts and business requirements.
 *
 * @author Samchon
 */
export interface AutoBeTestCorrectEvent
  extends AutoBeEventBase<"testCorrect">,
    AutoBeAggregateEventBase {
  kind: "casting" | "overall" | "request";

  /**
   * Function type indicating the specific test writing operation performed.
   *
   * This discriminated union represents different stages and types of test code
   * generation that occur during the test writing process:
   *
   * - `AutoBeTestWritePrepareFunction`: Generates test data preparation functions
   *   that create mock DTO objects required by API endpoints
   * - `AutoBeTestWriteGenerationFunction`: Creates resource generation functions
   *   that produce test data and utilities needed by test scenarios
   * - `AutoBeTestWriteAuthorizationFunction`: Implements authentication and
   *   authorization functions for different actors (login, signup, token
   *   refresh)
   * - `AutoBeTestWriteFunction`: Writes the actual E2E test scenario files with
   *   complete test implementations
   *
   * Each function type serves a specific purpose in building comprehensive test
   * suites, from data preparation through authentication to actual scenario
   * validation. The discriminated union pattern enables type-safe handling of
   * different test writing stages while providing detailed progress tracking.
   */
  function:
    | AutoBeTestWritePrepareFunction
    | AutoBeTestWriteGenerationFunction
    | AutoBeTestWriteAuthorizationFunction
    | AutoBeTestWriteFunction;

  /**
   * The compilation failure details that triggered the correction process.
   *
   * Contains the specific {@link IAutoBeTypeScriptCompileResult.IFailure}
   * information describing the compilation errors that were detected in the
   * test code. This includes error messages, file locations, type issues, or
   * other compilation problems that prevented successful test code validation.
   *
   * The failure information provides the diagnostic foundation for the AI's
   * understanding of what went wrong and guides the correction strategy.
   */
  result: IAutoBeTypeScriptCompileResult.IFailure;

  /**
   * AI's deep compilation error analysis and correction strategy.
   *
   * Contains the AI's comprehensive analysis of compilation errors and the
   * strategic approach for resolving them. This analysis examines each error
   * message to understand root causes, identifies error patterns, and develops
   * targeted correction strategies while maintaining the original test
   * purpose.
   *
   * The AI correlates compilation diagnostics with business requirements to
   * ensure that error corrections preserve the intended functionality. This
   * deep analysis forms the foundation for all subsequent correction efforts,
   * demonstrating the AI's ability to understand complex type errors and
   * develop systematic solutions.
   */
  think: string;

  /**
   * Iteration number of the requirements analysis this test correction was
   * performed for.
   *
   * Indicates which version of the requirements analysis this test correction
   * reflects. This step number ensures that the correction efforts are aligned
   * with the current requirements and helps track the quality improvement
   * process as compilation issues are resolved through iterative feedback.
   *
   * The step value enables proper synchronization between test correction
   * activities and the underlying requirements, ensuring that test improvements
   * remain relevant to the current project scope and validation objectives.
   */
  step: number;
}
